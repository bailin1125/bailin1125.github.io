---
title: 在 WSL2 里搭一套顺手的开发环境
description: 每次 Windows 重装后二十分钟恢复生产力的清单，外加几个踩过的坑。
pubDate: 2026-06-08
tags:
  - WSL
  - 工具
---

主力机是 Windows，开发全在 WSL2 里。重装过几次之后，把恢复环境的步骤固化成了一份清单。

## 基础层

```bash
sudo apt update && sudo apt install -y git curl build-essential
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
```

Node 用 nvm 管，Python 用 venv，不往系统目录里装东西，日后少很多麻烦。

## 踩过的坑

- **localhost 不通**：从 Windows 访问 WSL 里的服务有时要走 WSL 的 IP，`ip addr show eth0` 拿到地址再用；
- **文件别放 `/mnt/c`**：跨文件系统的 IO 很慢，代码一定放在 WSL 自己的 home 目录里；
- **git 换行符**：仓库里加一个 `.gitattributes`，省得 diff 满屏红。

## 一点心得

环境配置的价值在于「可重放」。凡是这次手工敲过的命令，下次就该进脚本——这次的重装清单，就是下次的一键脚本。
