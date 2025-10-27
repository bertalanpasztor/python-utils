from datetime import datetime
import time
import random
import threading
from time import sleep


def random_date(start, end):
    start_timestamp = int(time.mktime(start.timetuple()))
    end_timestamp = int(time.mktime(end.timetuple()))
    random_timestamp = random.randint(start_timestamp, end_timestamp)
    return datetime.datetime.fromtimestamp(random_timestamp)


def convert_to_radix(in_num, radix):
    UPPERCASE = [chr(i) for i in range(65, 65 + 26)]
    LOWERCASE = [chr(i) for i in range(97, 97 + 26)]
    ALL_LETTER = [chr(i) for i in range(48, 48 + 10)] + UPPERCASE + LOWERCASE
    if radix == 0:
        return None
    result = ""
    num = in_num
    while num != 0:
        num_div_radix = num // radix
        dig = ((num % radix) + radix) % radix
        result = ALL_LETTER[int(dig)] + result
        num = num_div_radix
    return result


def padd_l(text, length, padd_char):
    return text.rjust(length, padd_char)


class IDUtil:

    @staticmethod
    def generate_id():
        RADIX = 36
        DATE_2013_01_01 = 1356998400000
        x_ind = IDUtil.get_next_index()

        x_time = int((time.time() * 1000) - DATE_2013_01_01)
        x_res = convert_to_radix(x_time, RADIX)
        x_res = padd_l(x_res, 8, '0')

        nano = time.time_ns()
        x_nano = convert_to_radix(nano, RADIX)
        x_nano_part = x_nano[-4:]

        random_part = padd_l(convert_to_radix(random.randint(0, RADIX * RADIX - 1), RADIX), 2, '0')
        index_part = padd_l(convert_to_radix(x_ind, RADIX), 2, '0')

        return f"{x_res}{x_nano_part}{random_part}{index_part}"

    @staticmethod
    def get_next_index():
        RADIX = 36
        generated_index = 0
        generated_index_lock = threading.Lock()
        with generated_index_lock:
            generated_index += 1
            if generated_index > RADIX * RADIX - 1:
                generated_index = 0
            return generated_index

def generateid():
    # Generate random 5-digit integer (to match the original logic)
    rndint = random.randint(10000, 99999)
    idstr = datetime.now().strftime('%Y%m%d%H%M%S%f') + str(rndint)
    szam = int(idstr)
    szam_konv = ''
    while szam > 0:
        szamjegy = szam % 35
        if 0 <= szamjegy <= 9:
            szam_konv = chr(48 + szamjegy) + szam_konv
        elif 10 <= szamjegy <= 34:
            szam_konv = chr(65 + szamjegy - 10) + szam_konv
        szam = szam // 35
    return szam_konv

if __name__ == '__main__':
    for _ in range(10):
        sleep(0.001)
        print(generateid())
