# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 20:57:07 2021

@author: 박영신
"""

zip_file = open('myzip.zip', 'rb')

for i in range (40):
    zip_file.seek(i*4)
    r = list(zip_file.read(4))             #4개씩 읽기
    r.reverse()                            #little endian 위해 순서 바꾸기
    for j in range(len(r)):                
        r[j] = "{:02x}".format(r[j])
    r = '0x' + ''.join(r)                  #local file signature과 비교하기 위함
    if r == '0x04034b50':                  #local file signature
        offset_list=(i*4)                #local file signature과 같으면 offset_list에 추가
    elif r == '0x02014b50':                #central file signature
        break                              #local file을 다 읽은 후 break
    
local_file_signature_offset = offset_list
name_length_offset = local_file_signature_offset + 26   #file name 길이 정보 위치
extra_length_offset = name_length_offset + 2            #extra field 길이 정보 위치

zip_file.seek(name_length_offset)
name_length_before = zip_file.read(2)      #file name length는 2bytes를 차지하기 때문
name_length_after = list(name_length_before)
name_add = 0
for i in range (2):
    name_add += name_length_after[i]
name_length = name_add

zip_file.seek(extra_length_offset)         #extra filed length는 2bytes를 차지하기 때문
extra_length_before = zip_file.read(2)
extra_length_after = list(extra_length_before)
extra_add = 0
for i in range (2):
    extra_add += extra_length_after[i]
extra_length = extra_add

name_offset = extra_length_offset + 2          #name offset 
zip_file.seek(name_offset)
name_list = list(zip_file.read(name_length))   #name offset부터 name length만큼 읽기
for i in range(name_length):
    name_list[i] = chr(name_list[i])           #문자로 변환
name_list = ''.join(name_list)                 #변환한 문자 붙이기


data_offset = name_offset + name_length + extra_length    #data offset
zip_file.seek(data_offset)
data = zip_file.read(5)                                   #데이터 영역 읽기 
fw = open('data.txt', 'wb+')                              
fw.write(data)                                            #data.txt파일에 데이터 영역 저장
fw.close()

print('파일명: ', name_list)
print('파일 데이터 시작 offset : ', data_offset)

