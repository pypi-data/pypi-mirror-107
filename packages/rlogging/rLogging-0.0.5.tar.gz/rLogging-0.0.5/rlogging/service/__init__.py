""" Модуль реализации демона.

Демон запускается и выключается через консоль.
К демону обращается хендлер DaemonProcessHandler, после чего он передает лог в принтеры.


Для использования функционала демона, нужна библиотека `zmq`.


"""

try:
    import zmq

except ImportError:
    print('Для использования функционала "{}", нужен модуль "zmq".'.format(
        __name__.__module__
    ))
    print('use: pip install zmq')
    exit(1)

print(__name__.__module__)