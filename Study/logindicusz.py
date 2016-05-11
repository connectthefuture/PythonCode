import dns.resolver

resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8']
answer = resolver.query('www.xuli.co')
print(answer.response)