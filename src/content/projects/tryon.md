---
title: AI 虚拟试衣
description: 上传照片与服装，AI 生成换装效果：Flutter App + IDM-VTON 全链路 Demo。
status: development
longText: clothesShow 是一个虚拟试衣 Demo：Flutter 移动端拍照选衣，Node.js BFF 调度 Replicate 上的 IDM-VTON 模型生成换装结果，历史记录存 SQLite，对象存储走 R2/S3。围绕真实使用体验做了多轮打磨：试衣状态跨页面保持、结果默认平图可选沉浸查看、失败记录跳过深度图请求。
features:
  - IDM-VTON 换装生成，TTL 对齐的服务端任务管理
  - 历史记录缩略图与沉浸式查看器
  - Flutter App + Fastify BFF + SQLite + R2/S3 完整链路
tech:
  - Flutter
  - Fastify
  - Replicate
  - SQLite
featured: true
order: 3
---
