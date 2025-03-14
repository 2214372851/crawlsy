from enum import Enum


class Code(Enum):
    OK = 0

    # 操作已取消，通常由调用方取消。
    #
    # HTTP 映射：499 客户端关闭请求

    CANCELLED = 1

    # 未知错误。 例如，当以下情况下，可能会返回此错误
    # 从另一个地址空间接收的 'Status' 值属于
    # 此地址空间中未知的错误空间。 也
    # 接口未返回足够错误信息引发的错误
    # 可能会转换为此错误。
    #
    # HTTP 映射：500 内部服务器错误
    UNKNOWN = 2

    # 客户端指定了无效参数。 请注意，这是不同的
    # 来自 'FAILED_PRECONDITION'。 “INVALID_ARGUMENT”表示参数
    # 无论系统状态如何，都是有问题的
    # （例如，格式错误的文件名）。
    #
    # HTTP 映射：400 错误请求
    INVALID_ARGUMENT = 3

    # 在操作完成之前，截止时间已过期。对于操作
    # 更改系统状态时，可能会返回此错误
    # 即使操作已成功完成。 例如，一个
    # 来自服务器的成功响应可能会延迟很长时间
    # 足以让截止日期到期。
    #
    # HTTP 映射：504 网关超时
    DEADLINE_EXCEEDED = 4

    # 未找到某些请求的实体（例如，文件或目录）。
    #
    # 服务器开发人员注意事项：如果整个类的请求被拒绝
    # 的用户，例如逐步推出功能或未记录的允许列表，
    # 可以使用“NOT_FOUND”。如果某些用户的请求被拒绝
    # 一类用户，例如基于用户的访问控制，“PERMISSION_DENIED”
    # 必须使用。
    #
    # HTTP 映射：未找到 404
    NOT_FOUND = 5

    # 客户端尝试创建的实体（例如，文件或目录）
    # 已存在。
    #
    # HTTP 映射：409 冲突
    ALREADY_EXISTS = 6

    # 调用方没有权限执行指定的
    # 操作。“PERMISSION_DENIED”不得用于拒绝
    # 耗尽某些资源（使用“RESOURCE_EXHAUSTED”导致
    # 代替这些错误）。“PERMISSION_DENIED”不得为
    # 如果无法识别调用方，则使用（使用 'UNAUTHENTICATED'
    # 代替这些错误）。此错误代码并不意味着
    # 请求有效或请求实体存在或满足
    # 其他前提条件。
    #
    # HTTP 映射：403 禁止访问
    PERMISSION_DENIED = 7

    # 请求没有有效的身份验证凭据
    # 操作。
    #
    # HTTP 映射：401 未经授权
    UNAUTHENTICATED = 16

    # 某些资源已用尽，可能是每用户配额，或者
    # 也许整个文件系统空间不足。
    #
    # HTTP 映射：429 个请求太多
    RESOURCE_EXHAUSTED = 8

    # 由于系统未处于某个状态，操作被拒绝
    # 操作执行所必需。 例如，目录
    # 要删除的非空，则 rmdir 操作应用于
    # 非目录等。
    #
    # 服务实现者可以使用以下准则来决定
    # 在 'FAILED_PRECONDITION'、'ABORTED' 和 'UNAVAILABLE' 之间：
    # （a） 如果客户端只能重试失败的调用，则使用“UNAVAILABLE”。
    # （b） 如果客户端应该在更高级别重试，请使用“ABORTED”。为
    # 示例，当客户端指定的测试和设置失败时，表示
    # 客户端应该重启读-修-写序列。
    # （c） 如果客户端不应重试，则使用 'FAILED_PRECONDITION'，直到
    # 系统状态已显式修复。例如，如果“rmdir”
    # 失败，因为目录为非空，'FAILED_PRECONDITION'
    # 应该返回，因为客户端不应该重试，除非
    # 文件从目录中删除。
    #
    # HTTP 映射：400 错误请求
    FAILED_PRECONDITION = 9

    # 操作已中止，通常是由于并发问题，例如
    # 排序器检查失败或事务中止。
    #
    # 请参阅上面的指南，在“FAILED_PRECONDITION”之间做出决定，
    # '已中止'和'不可用'。
    #
    # HTTP 映射：409 冲突
    ABORTED = 10

    # 操作已超出有效范围。 例如，寻求或
    # 读取过去的文件末尾。
    #
    # 与 'INVALID_ARGUMENT' 不同，此错误表示可能存在的问题
    # 如果系统状态发生变化，则修复。例如，32 位文件
    # 系统将生成 'INVALID_ARGUMENT' 如果被要求读取
    # 不在 [0,2^32-1] 范围内的偏移量，但会生成
    # 'OUT_OF_RANGE' 如果被要求从电流过后的偏移量读取
    # 文件大小。
    #
    # “FAILED_PRECONDITION”和
    # 'OUT_OF_RANGE'。 我们建议使用“OUT_OF_RANGE”（更具体
    # error） 时，以便正在迭代的调用方
    # 一个空格可以很容易地寻找一个 'OUT_OF_RANGE' 错误来检测
    # 他们完成了。
    #
    # HTTP 映射：400 错误请求
    OUT_OF_RANGE = 11

    # 该操作未实现或不支持/启用
    # 服务。
    #
    # HTTP 映射：501 未实现
    UNIMPLEMENTED = 12

    # 内部错误。 这意味着
    # 底层系统已损坏。 此错误代码是保留的
    # 表示严重错误。
    #
    # HTTP 映射：500 内部服务器错误
    INTERNAL = 13

    # 该服务目前不可用。 这很可能是
    # 暂时性条件，可以通过重试来纠正
    # 退避。请注意，重试并不总是安全的
    # 非幂等运算。
    #
    # 请参阅上面的指南，在“FAILED_PRECONDITION”之间做出决定，
    # '已中止'和'不可用'。
    #
    # HTTP 映射：503 服务不可用
    UNAVAILABLE = 14

    # 不可恢复的数据丢失或损坏。
    #
    # HTTP 映射：500 内部服务器错误
    DATA_LOSS = 15
