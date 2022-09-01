import serial

dot_pad_sync = b'\xAA\x55'
dot_pad_20_len = b'\x00\x1A'
dot_pad_20_dest_id = b'\x00'
dot_pad_display_cmd = b'\x02\x00'
dot_pad_seq_num = b'\x80'
dot_pad_offset = b'\x00'

# 20셀 데이터를 위한 고정 header 값
dot_pad_display_header = dot_pad_sync + dot_pad_20_len + \
    dot_pad_20_dest_id + dot_pad_display_cmd + dot_pad_seq_num + dot_pad_offset

# 모든 점자 디스플레이를 올리는 점자 데이터
all_up_data = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
# 모든 점자 디스플레이를 내리는 점자 데이터
all_down_data = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

dot_pad_check_sum_len = 1
dot_pad_check_sum_offset = 4


def get_check_sum(buf, len):
    check_sum = int.from_bytes(b'\xA5', byteorder='big')

    for i in range(0, len):
        check_sum = check_sum ^ buf[i]

    return check_sum.to_bytes(1, byteorder='big')


# '/dev/ttyS0' -> 연결 환경에 따라 변경
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
ser.xonxoff = True
ser.rtscts = False
ser.dsrdtr = False
ser.write_timeout = 0

while True:
    inputStr = input("input: ")
    if inputStr == 'up':
        write_data = dot_pad_display_header + all_up_data
        check_sum = get_check_sum(
            write_data[dot_pad_check_sum_offset:], int.from_bytes(dot_pad_20_len, byteorder='big') - dot_pad_check_sum_len)
        ser.write(write_data + check_sum)
    elif inputStr == 'down':
        write_data = dot_pad_display_header + all_down_data
        check_sum = get_check_sum(
            write_data[dot_pad_check_sum_offset:], int.from_bytes(dot_pad_20_len, byteorder='big') - dot_pad_check_sum_len)
        ser.write(write_data + check_sum)
    elif inputStr == 'quit':
        break

ser.close()

# [20셀 데이터를 위한 고정 header 값 + 점자 데이터 + checksum]으로 데이터를 생성 후 write하여 점자 셀에 디스플레이
#
# 20셀 데이터를 위한 고정 header 값:
#   'dot_pad_display_header' 고정값 사용
# 점자 데이터:
#   점역 엔진에서 두 번째 파라미터 'output'을 사용, 20개 미만의 데이터가 생성되면 20개까지 나머지 부분은 0으로 채워서 저장
#   21개 이상의 데이터가 생성되면 20개 단위로 나누어 디스플레이
# checksum:
#   checksum 데이터를 제외한 '20셀 데이터를 위한 고정 header 값 + 점자 데이터'를 파라미터로 사용하여호출한 get_check_sum 함수의 리턴값
#
# e.g. 점역 엔진의 'input'을 '0xAC00, 0xB098, 0xB2E4, 0xB77C'로 하였을때, 'output' 데이터가 '0x2B, 0x09, 0x0A, 0x10, 0x23'으로 생성, 아래 값을 write
#   b'\xAA\x55\x00\x1A\x00\x02\x00\x80\x00\x2B\x09\x0A\x10\x23\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xD9'
#
# e.g. all_up_data를 점자 데이터로 사용할 경우 아래 값을 write
#   b'\xAA\x55\x00\x1A\x00\x02\x00\x80\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x27'
#
# e.g. all_down_data를 점자 데이터로 사용할 경우 아래와 같은 값을 write
#   b'\xAA\x55\x00\x1A\x00\x02\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x27'
