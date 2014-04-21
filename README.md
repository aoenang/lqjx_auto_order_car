lqjx_auto_order_car
===================

适用于龙泉驾校2014年4月后约车系统。基于Python2.7.3编写，自动循环发送约车请求。模拟网页手动操作。

请求输入参数:“username,password,jlcbh,xnsd”格式，通过username和password进行自动登录并去预约jlcbh对应的车辆，xnsh对应的时段。如果失败，会车号递增再次请求预约。如果预约成功，循环等待参数输入进行其他用户约车操作。
