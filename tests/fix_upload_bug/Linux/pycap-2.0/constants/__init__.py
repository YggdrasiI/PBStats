#__all__ = ['arp', 'ip', 'icmp', 'tcp', 'udp', 'ethernet', 'sll']
__all__ = ['arp', 'ip', 'icmp', 'tcp', 'udp', 'ethernet']

for module in __all__:
    setattr(__import__(__name__), module, __import__('%s.%s' % (__name__, module)))

del module
