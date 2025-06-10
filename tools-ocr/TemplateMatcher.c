#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

// 定义DLL导出宏
#ifdef __cplusplus
#define DLL_EXPORT extern "C" __declspec(dllexport)
#else
#define DLL_EXPORT __declspec(dllexport)
#endif

// 灰度图像结构体
typedef struct {
    int width;
    int height;
    unsigned char* data;
} GrayImage;

// 点坐标结构体
typedef struct {
    int x;
    int y;
    int error;  // 0表示成功，非0表示错误码
    double confidence; // 匹配置信度
} MatchResult;

// 屏幕截图并转换为灰度图像
DLL_EXPORT GrayImage* CaptureScreenGray(int* errorCode) {
    *errorCode = 0;
    HDC hdcScreen = GetDC(NULL);
    if (!hdcScreen) {
        *errorCode = 1;
        return NULL;
    }

    HDC hdcMem = CreateCompatibleDC(hdcScreen);
    if (!hdcMem) {
        ReleaseDC(NULL, hdcScreen);
        *errorCode = 2;
        return NULL;
    }

    int width = GetSystemMetrics(SM_CXSCREEN);
    int height = GetSystemMetrics(SM_CYSCREEN);
    
    HBITMAP hBitmap = CreateCompatibleBitmap(hdcScreen, width, height);
    if (!hBitmap) {
        ReleaseDC(NULL, hdcScreen);
        DeleteDC(hdcMem);
        *errorCode = 3;
        return NULL;
    }

    SelectObject(hdcMem, hBitmap);
    if (!BitBlt(hdcMem, 0, 0, width, height, hdcScreen, 0, 0, SRCCOPY)) {
        ReleaseDC(NULL, hdcScreen);
        DeleteDC(hdcMem);
        DeleteObject(hBitmap);
        *errorCode = 4;
        return NULL;
    }

    BITMAPINFOHEADER bmi = {0};
    bmi.biSize = sizeof(BITMAPINFOHEADER);
    bmi.biWidth = width;
    bmi.biHeight = -height;
    bmi.biPlanes = 1;
    bmi.biBitCount = 24;
    bmi.biCompression = BI_RGB;

    unsigned char* pixels = (unsigned char*)malloc(3 * width * height);
    if (!pixels) {
        ReleaseDC(NULL, hdcScreen);
        DeleteDC(hdcMem);
        DeleteObject(hBitmap);
        *errorCode = 5;
        return NULL;
    }

    if (!GetDIBits(hdcScreen, hBitmap, 0, height, pixels, (BITMAPINFO*)&bmi, DIB_RGB_COLORS)) {
        free(pixels);
        ReleaseDC(NULL, hdcScreen);
        DeleteDC(hdcMem);
        DeleteObject(hBitmap);
        *errorCode = 6;
        return NULL;
    }

    GrayImage* result = (GrayImage*)malloc(sizeof(GrayImage));
    if (!result) {
        free(pixels);
        ReleaseDC(NULL, hdcScreen);
        DeleteDC(hdcMem);
        DeleteObject(hBitmap);
        *errorCode = 7;
        return NULL;
    }

    result->width = width;
    result->height = height;
    result->data = (unsigned char*)malloc(width * height);
    if (!result->data) {
        free(pixels);
        free(result);
        ReleaseDC(NULL, hdcScreen);
        DeleteDC(hdcMem);
        DeleteObject(hBitmap);
        *errorCode = 8;
        return NULL;
    }
    
    #pragma omp parallel for
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int offset = y * width * 3 + x * 3;
            unsigned char r = pixels[offset + 2];
            unsigned char g = pixels[offset + 1];
            unsigned char b = pixels[offset];
            result->data[y * width + x] = (unsigned char)(0.299 * r + 0.587 * g + 0.114 * b);
        }
    }

    free(pixels);
    ReleaseDC(NULL, hdcScreen);
    DeleteDC(hdcMem);
    DeleteObject(hBitmap);

    return result;
}

// 加载PNG图像并转为灰度
DLL_EXPORT GrayImage* LoadImageGray(const char* filename, int* errorCode) {
    if (!errorCode) return NULL;
    *errorCode = 0;
    
    int width, height, channels;
    unsigned char* data = stbi_load(filename, &width, &height, &channels, 1);
    if (!data) {
        *errorCode = 100;
        return NULL;
    }

    GrayImage* result = (GrayImage*)malloc(sizeof(GrayImage));
    if (!result) {
        stbi_image_free(data);
        *errorCode = 101;
        return NULL;
    }

    result->width = width;
    result->height = height;
    result->data = data;
    return result;
}

// 带OpenMP加速和负载均衡的模板匹配
DLL_EXPORT MatchResult FindTemplateOptimized(GrayImage* screen, GrayImage* target, double threshold) {
    MatchResult result = {-1, -1, 0, 0.0};
    
    if (!screen || !target || !screen->data || !target->data) {
        result.error = 200;
        return result;
    }

    if (target->width > screen->width || target->height > screen->height) {
        result.error = 201;
        return result;
    }

    double minDiff = INFINITY;
    const int targetPixels = target->width * target->height;
    const long maxPossibleDiff = 255 * 255 * targetPixels;
    const int chunk_size = (target->height > 100) ? 5 : 10;

    #pragma omp parallel
    {
        double localMinDiff = INFINITY;
        int localBestX = -1;
        int localBestY = -1;

        #pragma omp for schedule(dynamic, chunk_size) nowait
        for (int y = 0; y <= screen->height - target->height; y++) {
            register long diff;
            register int screenPixel, targetPixel;

            for (int x = 0; x <= screen->width - target->width; x++) {
                diff = 0;
                
                for (int ty = 0; ty < target->height; ty++) {
                    const int screenY = y + ty;
                    const int targetYOffset = ty * target->width;
                    int tx = 0;

                    for (; tx < target->width - 3; tx += 4) {
                        screenPixel = screen->data[screenY * screen->width + x + tx];
                        targetPixel = target->data[targetYOffset + tx];
                        diff += (screenPixel - targetPixel) * (screenPixel - targetPixel);

                        screenPixel = screen->data[screenY * screen->width + x + tx + 1];
                        targetPixel = target->data[targetYOffset + tx + 1];
                        diff += (screenPixel - targetPixel) * (screenPixel - targetPixel);

                        screenPixel = screen->data[screenY * screen->width + x + tx + 2];
                        targetPixel = target->data[targetYOffset + tx + 2];
                        diff += (screenPixel - targetPixel) * (screenPixel - targetPixel);

                        screenPixel = screen->data[screenY * screen->width + x + tx + 3];
                        targetPixel = target->data[targetYOffset + tx + 3];
                        diff += (screenPixel - targetPixel) * (screenPixel - targetPixel);
                    }

                    for (; tx < target->width; tx++) {
                        screenPixel = screen->data[screenY * screen->width + x + tx];
                        targetPixel = target->data[targetYOffset + tx];
                        diff += (screenPixel - targetPixel) * (screenPixel - targetPixel);
                    }
                }

                if (diff < localMinDiff) {
                    localMinDiff = diff;
                    localBestX = x + target->width / 2;
                    localBestY = y + target->height / 2;
                }
            }
        }

        #pragma omp critical
        {
            if (localMinDiff < minDiff) {
                minDiff = localMinDiff;
                result.x = localBestX;
                result.y = localBestY;
            }
        }
    }

    result.confidence = 1.0 - ((double)minDiff / maxPossibleDiff);
    if (result.confidence < threshold) {
        result.x = -1;
        result.y = -1;
        result.error = 202;
    }

    return result;
}

// 鼠标点击
DLL_EXPORT int ClickAt(int x, int y) {
    if (!SetCursorPos(x, y)) {
        return 300;
    }

    INPUT inputs[2] = {{0}};
    inputs[0].type = INPUT_MOUSE;
    inputs[0].mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
    inputs[1].type = INPUT_MOUSE;
    inputs[1].mi.dwFlags = MOUSEEVENTF_LEFTUP;
    
    if (SendInput(2, inputs, sizeof(INPUT)) != 2) {
        return 301;
    }

    return 0;
}

// 释放图像内存
DLL_EXPORT void FreeGrayImage(GrayImage* img) {
    if (img) {
        if (img->data) {
            free(img->data);
        }
        free(img);
    }
}

// 初始化函数
DLL_EXPORT int Initialize() {
    omp_set_num_threads(omp_get_num_procs() * 2);
    return 0;
}