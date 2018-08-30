
# 协程的支持是通过generator实现的。
# 在generator中，我们不但可以通过for循环来迭代，还可以不断调用next()函数获取由yield语句返回的下一个值。
# 但是Python的yield不但可以返回一个值，它还可以接收调用者发出的参数。

# 来看例子：
# 传统的生产者-消费者模型是一个线程写消息，一个线程取消息，通过锁机制控制队列和等待，但一不小心就可能死锁。
# 如果改用协程，生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，切换回生产者继续生产，效率极高：

# 消费者
def consumer():
    r = ''
    while True:
        # 3 通过yield拿到消息，处理，又通过yield把结果传回
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

# 生产者
def produce(c):
    # 1 启动生成器：消费者
    c.send(None)    
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        # 2 切换到consumer执行 （3）
        r = c.send(n)
        # 拿到consumer处理的结果，继续生产下一条消息；
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)

# consumer函数是一个generator，把一个consumer传入produce后：

# 首先调用c.send(None)启动生成器；

# 然后，一旦生产了东西，通过c.send(n)切换到consumer执行；

# consumer通过yield拿到消息，处理，又通过yield把结果传回；

# produce拿到consumer处理的结果，继续生产下一条消息；

# produce不生产了，通过c.close()关闭consumer，整个过程结束。

# 整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务。