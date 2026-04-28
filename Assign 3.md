# COMPX234-A3：作业3说明书及任务拆解

## 一、 作业说明书全文翻译

[cite_start]**COMPX234-A3：作业3说明** [cite: 1]

[cite_start]**诚信。** 你将使用GitLab、GitHub或Gitee来展示你逐步开发的证据，并证明你理解了这项工作 [cite: 2][cite_start]。不允许使用LLM（大语言模型）提示来生成代码 [cite: 3][cite_start]。你必须清楚地解释你设计和实现的每一步，并通过GitLab/GitHub/Gitee中的提交（commits）来记录这些步骤 [cite: 4][cite_start]。如果提交历史未能展示出你的开发演进过程，该学生此项作业可能会得0分，和/或被要求参加口头答辩来解释代码 [cite: 5][cite_start]。此外，在期末考试中也需要展示对该实现的实际操作知识 [cite: 6][cite_start]。任何涉嫌作弊的案件都将交由学生纪律委员会进行调查 [cite: 7][cite_start]。我们承认代码生成是一个极其强大的工具，但在现阶段，学生需要在没有此类协助的情况下独立完成工作 [cite: 8][cite_start]。（郑重声明，我们也使用了不同的LLM生成了此作业的多个版本，我们将对使用LLM的迹象保持高度警惕。）相反，请向人类寻求帮助：去参加实验课，向在场的实验演示人员（demonstrators）提问以协助你的作业 [cite: 9]。

[cite_start]**日期与提交。** 本说明文档于2026年4月15日发布。提交截止日期为2026年4月30日，这对应于两周的工作量（总共约24小时的实践工作） [cite: 10][cite_start]。提交的内容将从GitLab、GitHub或Gitee提取 [cite: 11][cite_start]。我们将在作业批改开始前抓取最新的提交记录，这可能在截止日期后的任何时间发生（如果你拖延提交，你需要自行承担风险） [cite: 12]。

[cite_start]**概述。** 在此作业中，你将开发一个实现“元组空间（tuple space）”的客户端/服务器网络系统 [cite: 13][cite_start]。客户端发送请求以包含（写入）、读取或删除元组。服务器需要同时处理多个客户端 [cite: 14][cite_start]。每个客户端连接到服务器，开启“一个会话（session）”，并在会话期间发送一个或多个请求，直到其关闭 [cite: 15][cite_start]。发送请求后，客户端需要等待响应到达，然后再向服务器发送下一个请求 [cite: 16][cite_start]。这也就是我们所说的“同步行为”，它能简化客户端的实现 [cite: 17][cite_start]。在进行了一定数量的请求和响应之后，客户端终止会话并关闭连接 [cite: 18][cite_start]。服务器检测到客户端关闭了连接，也会随之结束与该客户端的会话 [cite: 19]。

[cite_start]**元组（Tuples）。** 服务器将实现一个“元组空间”。每个元组都是一个键值对（key-value pair），其中的键（key）和值（value）都是最多由999个字符组成的字符串 [cite: 20][cite_start]。键必须是唯一的，即不能存在两个具有相同键的元组 [cite: 21][cite_start]。你可以将其想象成一个简单的表格，包含两列：一列是键，一列是值 [cite: 22]。
[cite_start]这是一个元组空间的例子，在此例中是单词及其含义 [cite: 23]：

* [cite_start]**key** / **value** [cite: 24]
* [cite_start]"greeting" / "(usually plural) an acknowledgment or expression of good will (especially on meeting)" [cite: 24]
* [cite_start]"lighthouse" / "a tower with a light that gives warning of shoals to passing ships" [cite: 24]
* [cite_start]"Andre Maginot" / "French politician who proposed the Maginot Line (1877-1932)" [cite: 24]

[cite_start]服务器实现三种操作（这里使用颜色仅为增强可视化效果）： [cite: 25]

* [cite_start]$v=READ(k)$：如果存在键为k的元组，则读取元组 (k, v) 并返回值 v [cite: 26][cite_start]；如果k不存在，则操作失败且v返回空 [cite: 27]。
* [cite_start]$v=GET(k)$：如果存在键为k的元组，则删除元组 (k, v) 并返回值 v [cite: 28][cite_start]；如果k不存在，则操作失败且v返回空 [cite: 29]。
* [cite_start]$e=PUT(k,v)$：如果键k尚未存在，则将元组 (k, v) 添加到元组空间，e返回0 [cite: 30][cite_start]；如果键为k的元组已经存在，则操作失败，返回e等于1 [cite: 31]。

[cite_start]更准确地说，服务器的响应可以是： [cite: 32]

* [cite_start]OK (k, v) read [cite: 33]
* [cite_start]OK (k, v) removed [cite: 34]
* [cite_start]OK (k, v) added [cite: 35]
* [cite_start]ERR k already exists （当使用已存在的键k执行PUT操作时） [cite: 36]
* [cite_start]ERR k does not exist （当使用不存在的键k执行READ或GET操作时） [cite: 37]

[cite_start]**请求文件。** 客户端通过命令行启动，并接收一个包含请求的文本文件名作为其参数之一，文件每行一个请求 [cite: 38][cite_start]。例如，一个文件内容看起来像这样： [cite: 39]

* [cite_start]PUT Manchester-United 20 [cite: 40]
* [cite_start]PUT Liverpool 19 [cite: 41]
* [cite_start]PUT Arsenal 31 [cite: 42]
* [cite_start]PUT Everton 9 [cite: 43]
* [cite_start]PUT Manchester-City 9 [cite: 44]
* [cite_start]READ Liverpool [cite: 45]
* [cite_start]READ Arsenal [cite: 46]
* [cite_start]PUT Arsenal 13 [cite: 47]
* [cite_start]GET Arsenal [cite: 48]
* [cite_start]PUT Arsenal 13 [cite: 49]
* [cite_start]GET Manchester-United [cite: 50]
* [cite_start]READ Manchester-United [cite: 51]

[cite_start]通常规定，k和v的“组合大小”（作为一个由空格分隔的单一字符串）不能超过970个字符 [cite: 52][cite_start]。如果客户端的输入文件违反了此条件，需输出错误信息并忽略该条目 [cite: 53]。

[cite_start]**客户端输出。** 在客户端运行过程中，针对处理的每一行，客户端将显示所执行的操作及其结果 [cite: 54, 55][cite_start]。例如，从一个空的元组空间开始，输出将是： [cite: 55]

* [cite_start]PUT Manchester-United 20: OK (Manchester-United, 20) added [cite: 56]
* [cite_start]PUT Liverpool 19: OK (Liverpool, 19) added [cite: 57]
* [cite_start]PUT Arsenal 31: OK (Arsenal, 31) added [cite: 58]
* [cite_start]PUT Everton 9: OK (Everton, 9) added [cite: 59]
* [cite_start]PUT Manchester-City 9: OK (Manchester-City, 9) added [cite: 60]
* [cite_start]READ Liverpool: OK (Liverpool, 19) read [cite: 61]
* READ Arsenal: OK (Arsenal, 31) read
[cite_start]PUT Arsenal 13: ERR Arsenal exists [cite: 62]
* GET Arsenal: OK (Arsenal, 31) removed
PUT Arsenal 13: OK (Arsenal, 13) added [cite: 63]
* GET Manchester-United: OK (Manchester-United, 20) removed [cite: 64]
* READ Manchester-United: ERR Manchester-United does not exist [cite: 65]

[cite_start]在上述示例中，值v是每个俱乐部的英超联赛冠军数量，但它也可以是一个句子（支持最多992个可打印字符的任意字符串，包括空格） [cite: 66]。

[cite_start]**服务器输出。** 服务器端需要每10秒显示一次当前元组空间的摘要，包含：元组空间中的元组数量、平均元组大小、平均键大小、平均值（字符串）大小、到目前为止已连接的客户端总数（无论是否已断开）、总操作次数、总READ次数、总GET次数、总PUT次数以及错误数量 [cite: 67]。

[cite_start]**多线程服务器。** 如上所述，服务器需要同时处理与多个客户端的会话 [cite: 68][cite_start]。为此，服务器将使用多线程，创建一个新线程来处理每一个单独的客户端 [cite: 69][cite_start]。这比交错处理多个客户端的请求要使服务器的实现简单得多 [cite: 70][cite_start]。每当有新客户端连接到服务器时，服务器都会生成一个新线程 [cite: 71][cite_start]。当与客户端的会话/连接关闭时，该线程终止 [cite: 72]。

[cite_start]**客户端和服务器的命令行参数。** 你首先启动服务器，并提供服务器用于等待传入连接的端口号 [cite: 73][cite_start]。这必须是一个高位端口，例如51234（50000 <= 端口号 <= 59999） [cite: 74][cite_start]。在另一台主机上，你启动每个客户端。客户端接收三个参数： [cite: 75]

1. [cite_start]服务器所在的主机名（如果客户端和服务器在同一台主机上，则可以是“localhost”） [cite: 76]；
2. [cite_start]连接服务器的端口号（与服务器使用的值相同） [cite: 77]；
3. [cite_start]包含待处理（发送到服务器）请求的文本文件的路径名，格式如前文所述 [cite: 78]。

[cite_start]**使用TCP套接字的多线程服务器。** 本作业的重点是使用TCP套接字实现具有三种支持操作（READ、GET和PUT）的客户端/服务器协议，并实现一个即使在线程并发访问（共享）元组空间的情况下也能正确执行这些操作的服务器 [cite: 79][cite_start]。你的实现必须严格遵守该协议，因为你的客户端和服务器应该能够与其他学生开发的服务器和客户端进行互操作（interoperate） [cite: 80]。

[cite_start]**协议。** 要实现的协议对请求消息进行如下编码： [cite: 81]

* [cite_start]NNN R k [cite: 82]
* [cite_start]NNN G k [cite: 83]
* [cite_start]NNN P k v [cite: 84]

[cite_start]NNN是三个字符，表示消息的总大小，第一个字母表示命令（R代表READ，G代表GET，P代表PUT），k是键，v是值 [cite: 85][cite_start]。最小尺寸为7（即在READ/GET操作中，键k只有单个字符时），最大尺寸为999 [cite: 86]。
[cite_start]可传输到服务器的请求消息示例： [cite: 87]

* [cite_start]007 R a [cite: 88]
* [cite_start]010 R abcd [cite: 89]
* [cite_start]012 G 123456 [cite: 90]
* [cite_start]053 P good-morning-message how are you feeling today? [cite: 91]

[cite_start]响应消息（与前面定义的保持一致）也是使用字符串实现的，其格式为以下之一： [cite: 92]

* [cite_start]NNN OK (k, v) read [cite: 93]
* [cite_start]NNN OK (k, v) removed [cite: 94]
* [cite_start]NNN OK (k, v) added [cite: 95]
* [cite_start]NNN ERR k already exists [cite: 96]
* [cite_start]NNN ERR k does not exist [cite: 97]

[cite_start]示例（如果k和v都是单个字母数字字符）： [cite: 98]

* [cite_start]018 OK (k, v) read [cite: 99]
* [cite_start]021 OK (k, v) removed [cite: 100]
* [cite_start]014 OK k added [cite: 101]
* [cite_start]024 ERR k already exists [cite: 102]
* [cite_start]024 ERR k does not exist [cite: 103]

[cite_start]**编程语言。** 代码必须使用Python开发（如果需要，可以使用“面向对象”的方式） [cite: 104][cite_start]。开发必须基于讲座中探索/解释的特性，例如在Java开发中的“synchronized”关键字（注：在此是指并发同步控制机制） [cite: 105]。

[cite_start]**如何测试你的网络系统。** 我们提供了给客户端使用的示例文件，以及每个客户端和服务器的预期输出 [cite: 106][cite_start]。在测试中，元组空间包含100个不同的单词（来自英语词典） [cite: 107][cite_start]。每个文件有100,000个请求 [cite: 108]。
[cite_start]请遵循以下步骤： [cite: 109]
[cite_start]1) 在一台主机上启动服务器 [cite: 110]
[cite_start]2) 依次运行所有客户端（例如，在Python中可以是 `for i in {1..10}; do python myclient.py server 51234 client-$i.txt; done`） [cite: 111, 112]
[cite_start]3) 注意观察客户端产生的输出，特别是服务器的输出 [cite: 113]
[cite_start]4) 关闭服务器 (^c) 并重新启动 [cite: 114]
[cite_start]5) 并行运行所有客户端（例如，在Python中可以是 `for i in {1..10}; do python myclient.py server 51234 client-$i.txt &; done`） [cite: 115, 116]
[cite_start]6) 注意观察服务器产生的输出 [cite: 117]

[cite_start]**评分标准。** 你在GitLab、GitHub或Gitee中的项目必须命名为“COMPX234-A3” [cite: 118]。

* [cite_start]开发历史（每次提交步子要小，包含详细的提交信息）：20分 [cite: 119]
* [cite_start]代码质量（文档注释、代码缩进）：10分 [cite: 119]
* [cite_start]通过提供测试文件的所有测试：50分 [cite: 119]
* [cite_start]通过所有额外测试（未提供的测试用例，但将探索竞争条件/资源抢占和边界情况）：20分 [cite: 119]

---

## 二、 完成作业需要注意的核心事项

为了顺利完成此作业并获得高分，你需要特别注意以下几点：

1. [cite_start]**绝对禁止使用AI/LLM工具生成代码**：教师团队已经使用多种LLM生成了代码库以作比对，并且会使用反作弊手段进行审查 [cite: 3, 8, 9]。你必须亲自手写代码。
2. [cite_start]**强制要求使用Git并维持细粒度的提交历史**：这是防止作弊的核心机制，且独占20分。你必须在GitLab、GitHub或Gitee上持续提交（commit）代码，做到“小步快跑”，并在commit message中清晰记录每次代码的设计和实现思路 [cite: 2, 4, 119][cite_start]。如果只有少数几次大提交，不仅可能拿不到这20分，甚至可能整份作业被判0分或被叫去进行代码答辩 [cite: 5]。
3. **技术栈要求**：
    * [cite_start]**语言**：必须使用 Python 进行开发 [cite: 104]。
    * [cite_start]**通信协议**：必须使用底层的 TCP Sockets，且严格遵循文档中规定的 `NNN COMMAND Key Value` 的自定义字符串协议格式进行消息封包和解包 [cite: 79, 81, 85]。不能使用HTTP或其他高级库。
4. **多线程与并发控制（重中之重）**：
    * [cite_start]服务器必须是多线程的，每接入一个客户端就为其生成一个独立的线程 [cite: 68, 69, 71]。
    * [cite_start]**线程安全（Thread Safety）**：由于多个线程（代表不同的客户端）会同时去读取或修改同一个“元组空间（字典或表格）”，你必须使用同步原语（如 Python 中的 `threading.Lock`）来防止资源竞争（Race Conditions） [cite: 79, 105, 119][cite_start]。评分的最后20分专门用于测试并发竞争条件 [cite: 119]。
5. **严格处理边界情况与错误**：
    * [cite_start]k 和 v 的总长度（包含中间的空格）不能超过 970 个字符。超过这个限制，客户端不能向服务器发送，而是直接抛出错误并跳过这一行 [cite: 52, 53]。
    * [cite_start]确保消息的前三个字符 `NNN` 准确计算并包括了整条消息的长度（最小为7，最大为999） [cite: 85, 86]。
6. [cite_start]**定期统计信息打印**：服务器必须每隔 10 秒钟精准输出一次系统的运行状态统计，包括连接总数、总操作数、各类操作分类统计和平均长度等 [cite: 67]。

---

## 三、 最终需要交付的内容

[cite_start]在 **2026年4月30日** 截止日期之前 [cite: 10]，你需要交付以下内容：

1. **一个远程代码仓库**：
    * [cite_start]必须托管在 GitLab、GitHub 或 Gitee 上 [cite: 2, 11]。
    * [cite_start]仓库名称必须严格命名为 **`COMPX234-A3`** [cite: 118]。
2. **完整的开发历史记录**：
    * [cite_start]仓库中必须包含详细的、小步提交的 Git Commit 历史，且带有详尽的提交说明 [cite: 4, 118, 119]。
3. **Python 源代码文件**：
    * [cite_start]包含服务器端程序代码（实现多线程、TCP Socket监听、元组空间数据结构、并发锁、每10秒打印统计信息的逻辑） [cite: 67, 69, 79, 104]。
    * [cite_start]包含客户端程序代码（实现读取文本文件、通过TCP连接服务器、按要求格式化发送请求、阻塞等待响应、打印处理结果的逻辑） [cite: 16, 38, 54, 79, 104]。
    * [cite_start]良好的代码结构和质量（包括代码注释/文档、良好的缩进和命名规范） [cite: 119]。
