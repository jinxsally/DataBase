## 买家下单

#### URL：

POST http://[address]/buyer/new_order

#### Request

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
  "user_id": "buyer_id",
  "store_id": "store_id",
  "books": [
    {
      "id": "1000067",
      "count": 1
    },
    {
      "id": "1000134",
      "count": 4
    }
  ]
}
```

##### 属性说明：

| 变量名   | 类型   | 描述         | 是否可为空 |
| -------- | ------ | ------------ | ---------- |
| user_id  | string | 买家用户 ID  | N          |
| store_id | string | 商铺 ID      | N          |
| books    | class  | 书籍购买列表 | N          |

books 数组：

| 变量名 | 类型   | 描述      | 是否可为空 |
| ------ | ------ | --------- | ---------- |
| id     | string | 书籍的 ID | N          |
| count  | string | 购买数量  | N          |

#### Response

Status Code:

| 码  | 描述               |
| --- | ------------------ |
| 200 | 下单成功           |
| 5XX | 买家用户 ID 不存在 |
| 5XX | 商铺 ID 不存在     |
| 5XX | 购买的图书不存在   |
| 5XX | 商品库存不足       |

##### Body:

```json
{
  "order_id": "uuid"
}
```

##### 属性说明：

| 变量名   | 类型   | 描述                          | 是否可为空 |
| -------- | ------ | ----------------------------- | ---------- |
| order_id | string | 订单号，只有返回 200 时才有效 | N          |

## 买家付款

#### URL：

POST http://[address]/buyer/payment

#### Request

##### Body:

```json
{
  "user_id": "buyer_id",
  "order_id": "order_id",
  "password": "password"
}
```

##### 属性说明：

| 变量名   | 类型   | 描述         | 是否可为空 |
| -------- | ------ | ------------ | ---------- |
| user_id  | string | 买家用户 ID  | N          |
| order_id | string | 订单 ID      | N          |
| password | string | 买家用户密码 | N          |

#### Response

Status Code:

| 码  | 描述         |
| --- | ------------ |
| 200 | 付款成功     |
| 5XX | 账户余额不足 |
| 5XX | 无效参数     |
| 401 | 授权失败     |

## 买家充值

#### URL：

POST http://[address]/buyer/add_funds

#### Request

##### Body:

```json
{
  "user_id": "user_id",
  "password": "password",
  "add_value": 10
}
```

##### 属性说明：

| key       | 类型   | 描述                 | 是否可为空 |
| --------- | ------ | -------------------- | ---------- |
| user_id   | string | 买家用户 ID          | N          |
| password  | string | 用户密码             | N          |
| add_value | int    | 充值金额，以分为单位 | N          |

Status Code:

| 码  | 描述     |
| --- | -------- |
| 200 | 充值成功 |
| 401 | 授权失败 |
| 5XX | 无效参数 |

## 查看历史订单

该接口用于查询指定买家的历史订单，包括订单的状态、订单 ID、买家 ID、商家 ID、总价以及订单详情。

#### URL

GET http://[address]/buyer/hist_order

#### 请求参数

- `user_id` (string): 买家用户 ID，用于指定要查询的买家。

#### 响应

##### Body:

```json
{
  "user_id": "buyer_id",
  "order_id": "order_id",
  "password": "password"
}
```

##### 属性说明：

| key         | 类型   | 描述                                                                                                                                                             | 是否可为空 |
| ----------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| buyer_id    | string | 买家用户 ID                                                                                                                                                      | N          |
| password    | string | 用户密码                                                                                                                                                         | N          |
| order_id    | string | 订单 ID                                                                                                                                                          | N          |
| store_id    | string | 店铺 ID                                                                                                                                                          | N          |
| total_price | double | 用户密码                                                                                                                                                         | N          |
| details     | string | 订单详情，包含具体的商品信息和数量等。                                                                                                                           | N          |
| status      | string | 订单状态，可能的值包括 "unpaid"（未付款）、"unsent"（已付款但未发货）、"sent but not received"（已发货但未接收）、"received"（已接收）和 "cancelled"（已取消）。 | N          |

Status Code:

| 码  | 描述              |
| --- | ----------------- |
| 200 | 请求成功          |
| 528 | PyMongoError 错误 |
| 530 | 其他异常错误      |

## 取消订单

该接口用于取消指定订单。

#### URL

GET http://[address]/buyer/cancell_order

#### 请求参数

- `user_id` (string): 买家用户 ID，用于指定要查询的买家。

#### 响应

##### Body:

```json
{
  "user_id": "buyer_id",
  "order_id": "order_id"
}
```

##### 属性说明：

| key      | 类型   | 描述        | 是否可为空 |
| -------- | ------ | ----------- | ---------- |
| buyer_id | string | 买家用户 ID | N          |
| order_id | string | 订单 ID     | N          |

Status Code:

| 码  | 描述              |
| --- | ----------------- |
| 200 | 请求成功          |
| 528 | PyMongoError 错误 |
| 530 | 其他异常错误      |

## 自动取消订单

该接口用于自动取消指定订单。

#### URL

GET http://[address]/buyer/auto_cancell_order

#### 请求参数

- 无

#### 响应

##### Body:

```json
{
  "user_id": "buyer_id",
  "order_id": "order_id"
}
```

##### 属性说明：

| key      | 类型   | 描述        | 是否可为空 |
| -------- | ------ | ----------- | ---------- |
| buyer_id | string | 买家用户 ID | N          |
| order_id | string | 订单 ID     | N          |

Status Code:

| 码  | 描述                 |
| --- | -------------------- |
| 200 | 自动取消订单操作成功 |
| 528 | PyMongoError 错误    |
| 530 | 其他异常错误         |
