# #input1 = [1,2,3,4,5,6,7,8,9]

# for i in range(10):
#     print (i)
# for i in range(18):
#     print('{0:3} {1:18}'.format(i, 10**i))

# import phonenumbers
# from text import number
# from phonenumbers import geocoder, carrier


# ch_numb= phonenumbers.parse(number, "CH")
# print(geocoder.description_for_number(ch_numb, "en"))
# serv = phonenumbers.parse(number, "RO")
# print(carrier.name_for_number(serv, "en"))
camp = ""
for x in range(5):
    camp += str(x)
print(camp) #error printing because python cannot concatenate string to integer