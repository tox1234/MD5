# MD5

![image](https://github.com/user-attachments/assets/a6ada340-d38b-4232-b9f9-cf8e2faad0cf)


protocol explanation:

start_len + "!" + start + end_len + "!" + end + cmd_len + "!" + cmd + encode_len + "!" + encode

start_len = the length of the start

start = the start of the range of numbers

end_len = the length of the end

end = the end of the range of numbers

cmd_len = the length of the cmd

cmd = which cmd we want to do(encrypt,decrypt)

encode_len = the length of the encode

encode = the encryption we want to match with
