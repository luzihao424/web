# GitHub Issues Importer for "校园闲置时光胶囊"
$Owner = "luzihao424"
$Repo = "web"

# Request token from user
$Token = Read-Host -Prompt "请输入您的 GitHub Personal Access Token (PAT) [需包含 repo 权限]"

if (-not $Token) {
    Write-Error "Token 不能为空！"
    exit
}

$Issues = @(
    @{
        title = "[用户] 实现学号/手机号极简登录与会话保持"
        body = "作为访问用户，我想要输入学号或手机号进行极简登录，以便于快速进入系统并保留我的登录状态。"
    },
    @{
        title = "[用户] 个人中心基础页面与我的发布/收藏列表"
        body = "作为注册用户，我想要在个人中心查看我自己发布的物品和收藏的物品，以便于统一管理我参与的内容。"
    },
    @{
        title = "[用户] 用户隐私设置与账号管理"
        body = "作为注重隐私的用户，我想要设置我的联系方式可见范围，以便于在线下对接前保护我的个人隐私。"
    },
    @{
        title = "[发布] 物品发布页设计与发布接口 (含胶囊故事与交换类型)"
        body = "作为想要分享闲置物品的用户，我想要发布物品时必须填写“胶囊故事”，并选择交换类型（换物/借用/赠送），以便于他人了解物品背后的故事并选择合适的方式交换。"
    },
    @{
        title = "[展示] 响应式首页开发 (热门故事与闲置物品流)"
        body = "作为平台访问者，我想要在首页浏览热门的故事和最新的闲置物品列表（适配手机与PC），以便于快速发现感兴趣的物品和背后的治愈故事。"
    },
    @{
        title = "[展示] 物品详情页开发 (包含完整故事与申请组件)"
        body = "作为对某件闲置感兴趣的用户，我想要查看该物品的详细信息和完整的胶囊故事，以便于决定是否发起交换申请。"
    },
    @{
        title = "[互动] 发起留言申请与申请列表管理"
        body = "作为申请者，我想要针对心仪物品填写留言申请，以便于向发布者说明我的交换意愿或交换方案。"
    },
    @{
        title = "[互动] 线上对接标记与状态流转"
        body = "作为物品发布者，我想要在收到申请后选择接受，并提供线下对接方式（如微信号/QQ），并在对接完成后标记为“已完成”，以便于推进交换流程。"
    },
    @{
        title = "[互动] 自动生成交换日志与展示"
        body = "作为参与交换的双方，我想要在交换完成后系统自动生成一份“交换日志”（记录时间与温暖交接），以便于记录这段温暖的校园邂逅。"
    },
    @{
        title = "[胶囊] 匿名化处理逻辑与归档"
        body = "作为已完成交换的用户，我想要系统在交换完成后自动隐去我与对方的个人敏感信息，将物品故事归档为匿名，以便于保护隐私并为故事墙积累素材。"
    },
    @{
        title = "[胶囊] 治愈系时光胶囊匿名故事墙页面"
        body = "作为喜欢阅读故事的用户，我想要在一个专门的“时光胶囊故事墙”页面，以匿名卡片流的形式浏览所有已完成交换的物品背后的故事，以便于感受校园内的轻暖氛围。"
    }
)

$Headers = @{
    "Accept" = "application/vnd.github+json"
    "Authorization" = "Bearer $Token"
    "X-GitHub-Api-Version" = "2022-11-28"
}

Write-Host "开始导入 Issues 到 $Owner/$Repo ..." -ForegroundColor Cyan

foreach ($Issue in $Issues) {
    $BodyJson = $Issue | ConvertTo-Json -Compress
    Write-Host "正在创建: $($Issue.title)..."
    try {
        $Response = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo/issues" -Method Post -Headers $Headers -Body $BodyJson -ContentType "application/json; charset=utf-8"
        Write-Host "成功创建 Issue #$($Response.number)" -ForegroundColor Green
    } catch {
        Write-Error "创建失败: $_"
    }
    # 稍微等待，防止触发 API 频率限制
    Start-Sleep -Milliseconds 500
}

Write-Host "所有 Issues 导入完成！" -ForegroundColor Green
