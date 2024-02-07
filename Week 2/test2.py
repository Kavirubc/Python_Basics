#dictionaries


dic1={"Name":"John","Age":25}

print(dic1["Name"])

dic1['phonr']=1234567890

print(dic1)


print(dic1.keys())
print(dic1.values())

print('Name' in dic1)

print('Name' not in dic1)

print(dic1.get('Name'))
#search a value inside the dictornary
print(dic1.get('Name1', 'Not Found'))