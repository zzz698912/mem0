---
trigger: model_decision
description: openmemory
---

# OpenMemory 项目规则文件

## 项目概述
OpenMemory 是一个记忆管理平台，分为两个主要部分：
- 后端 API 服务（Python/FastAPI）
- 前端用户界面（React/Next.js）

## 技术栈规范

### 后端 API（openmemory/api）
- 使用 FastAPI 框架构建 RESTful API
- 数据库采用 SQLAlchemy ORM
- 使用 Alembic 进行数据库迁移
- 支持 CORS 跨域请求

### 前端 UI（openmemory/ui）
- 使用 Next.js 15（支持 React 19）
- TypeScript 语言
- TailwindCSS 样式框架
- Redux 状态管理
- Radix UI 组件库

## 后端功能模块

### 内存管理模块 (memories.py)
- 列出所有记忆内容
- 支持按时间、类别、应用等条件过滤
- 支持分页和搜索功能
- 提供分类统计

### 应用管理模块 (apps.py)
- 应用的增删改查
- 应用与用户的关联管理

### 统计信息模块 (stats.py)
- 统计用户总记忆数和连接的应用数

### 备份功能模块 (backup.py)
- 支持数据导出和导入

### 权限控制
- 实现了访问控制列表（ACL）机制
- 控制应用对记忆的访问权限

## 核心数据模型

1. 用户(User)：系统用户
2. 应用(App)：接入系统的第三方应用
3. 记忆(Memory)：用户存储的信息
4. 分类(Category)：记忆的分类标签
5. 访问控制(AccessControl)：权限控制规则

## 前端组件规范

### 主要页面和组件
- 仪表板页面 (page.tsx)：显示安装指引、统计数据和内存过滤浏览功能
- 统计组件 (Stats.tsx)：显示总记忆数和连接应用数，展示最近连接的应用图标
- 内存管理相关组件：内存过滤器、内存列表展示

### 数据交互规范
- 使用 axios 与后端 API 通信
- 自定义 hooks（如 useStats）处理 API 调用
- Redux 管理全局状态（用户信息、应用列表等）

## 架构特点

1. 前后端分离：API 和 UI 完全独立，通过 RESTful 接口通信
2. 容器化部署：提供了 Dockerfile 和 docker-compose 配置
3. 可扩展性：模块化的路由设计便于功能扩展
4. 权限安全：实现细粒度的访问控制
5. 现代化技术栈：使用最新的前端和后端技术

## 开发规范

1. 所有敏感信息（如 API 密钥）必须通过环境变量引用，格式为 `env:VARIABLE_NAME`
2. 模型参数应根据具体用途进行优化调整
3. 配置结构保持清晰层次，便于维护和扩展
4. 代码注释应当清晰说明业务逻辑和实现细节
5. 遵循 RESTful API 设计原则
