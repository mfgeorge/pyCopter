
try:
    import utime
except ImportError:
    import sys
    # Add some dummy libraries
    sys.path.insert(0, '../dummy_libraries')
    from dummy_libraries import utime

# I2C addresses
BNO055_ADDRESS_A                     = 0x28
BNO055_ADDRESS_B                     = 0x29
BNO055_ID                            = 0xA0

# Page id register definition
BNO055_PAGE_ID_ADDR                  = 0X07

# PAGE0 REGISTER DEFINITION START
BNO055_CHIP_ID_ADDR                  = 0x00
BNO055_ACCEL_REV_ID_ADDR             = 0x01
BNO055_MAG_REV_ID_ADDR               = 0x02
BNO055_GYRO_REV_ID_ADDR              = 0x03
BNO055_SW_REV_ID_LSB_ADDR            = 0x04
BNO055_SW_REV_ID_MSB_ADDR            = 0x05
BNO055_BL_REV_ID_ADDR                = 0X06

# Accel data register
BNO055_ACCEL_DATA_X_LSB_ADDR         = 0X08
BNO055_ACCEL_DATA_X_MSB_ADDR         = 0X09
BNO055_ACCEL_DATA_Y_LSB_ADDR         = 0X0A
BNO055_ACCEL_DATA_Y_MSB_ADDR         = 0X0B
BNO055_ACCEL_DATA_Z_LSB_ADDR         = 0X0C
BNO055_ACCEL_DATA_Z_MSB_ADDR         = 0X0D

# Mag data register
BNO055_MAG_DATA_X_LSB_ADDR           = 0X0E
BNO055_MAG_DATA_X_MSB_ADDR           = 0X0F
BNO055_MAG_DATA_Y_LSB_ADDR           = 0X10
BNO055_MAG_DATA_Y_MSB_ADDR           = 0X11
BNO055_MAG_DATA_Z_LSB_ADDR           = 0X12
BNO055_MAG_DATA_Z_MSB_ADDR           = 0X13

# Gyro data registers
BNO055_GYRO_DATA_X_LSB_ADDR          = 0X14
BNO055_GYRO_DATA_X_MSB_ADDR          = 0X15
BNO055_GYRO_DATA_Y_LSB_ADDR          = 0X16
BNO055_GYRO_DATA_Y_MSB_ADDR          = 0X17
BNO055_GYRO_DATA_Z_LSB_ADDR          = 0X18
BNO055_GYRO_DATA_Z_MSB_ADDR          = 0X19

# Euler data registers
BNO055_EULER_H_LSB_ADDR              = 0X1A
BNO055_EULER_H_MSB_ADDR              = 0X1B
BNO055_EULER_R_LSB_ADDR              = 0X1C
BNO055_EULER_R_MSB_ADDR              = 0X1D
BNO055_EULER_P_LSB_ADDR              = 0X1E
BNO055_EULER_P_MSB_ADDR              = 0X1F

# Quaternion data registers
BNO055_QUATERNION_DATA_W_LSB_ADDR    = 0X20
BNO055_QUATERNION_DATA_W_MSB_ADDR    = 0X21
BNO055_QUATERNION_DATA_X_LSB_ADDR    = 0X22
BNO055_QUATERNION_DATA_X_MSB_ADDR    = 0X23
BNO055_QUATERNION_DATA_Y_LSB_ADDR    = 0X24
BNO055_QUATERNION_DATA_Y_MSB_ADDR    = 0X25
BNO055_QUATERNION_DATA_Z_LSB_ADDR    = 0X26
BNO055_QUATERNION_DATA_Z_MSB_ADDR    = 0X27

# Linear acceleration data registers
BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR  = 0X28
BNO055_LINEAR_ACCEL_DATA_X_MSB_ADDR  = 0X29
BNO055_LINEAR_ACCEL_DATA_Y_LSB_ADDR  = 0X2A
BNO055_LINEAR_ACCEL_DATA_Y_MSB_ADDR  = 0X2B
BNO055_LINEAR_ACCEL_DATA_Z_LSB_ADDR  = 0X2C
BNO055_LINEAR_ACCEL_DATA_Z_MSB_ADDR  = 0X2D

# Gravity data registers
BNO055_GRAVITY_DATA_X_LSB_ADDR       = 0X2E
BNO055_GRAVITY_DATA_X_MSB_ADDR       = 0X2F
BNO055_GRAVITY_DATA_Y_LSB_ADDR       = 0X30
BNO055_GRAVITY_DATA_Y_MSB_ADDR       = 0X31
BNO055_GRAVITY_DATA_Z_LSB_ADDR       = 0X32
BNO055_GRAVITY_DATA_Z_MSB_ADDR       = 0X33

# Temperature data register
BNO055_TEMP_ADDR                     = 0X34

# Status registers
BNO055_CALIB_STAT_ADDR               = 0X35
BNO055_SELFTEST_RESULT_ADDR          = 0X36
BNO055_INTR_STAT_ADDR                = 0X37

BNO055_SYS_CLK_STAT_ADDR             = 0X38
BNO055_SYS_STAT_ADDR                 = 0X39
BNO055_SYS_ERR_ADDR                  = 0X3A

# Unit selection register
BNO055_UNIT_SEL_ADDR                 = 0X3B
BNO055_DATA_SELECT_ADDR              = 0X3C

# Mode registers
BNO055_OPR_MODE_ADDR                 = 0X3D
BNO055_PWR_MODE_ADDR                 = 0X3E

BNO055_SYS_TRIGGER_ADDR              = 0X3F
BNO055_TEMP_SOURCE_ADDR              = 0X40

# Axis remap registers
BNO055_AXIS_MAP_CONFIG_ADDR          = 0X41
BNO055_AXIS_MAP_SIGN_ADDR            = 0X42

# Axis remap values
AXIS_REMAP_X                         = 0x00
AXIS_REMAP_Y                         = 0x01
AXIS_REMAP_Z                         = 0x02
AXIS_REMAP_POSITIVE                  = 0x00
AXIS_REMAP_NEGATIVE                  = 0x01

# SIC registers
BNO055_SIC_MATRIX_0_LSB_ADDR         = 0X43
BNO055_SIC_MATRIX_0_MSB_ADDR         = 0X44
BNO055_SIC_MATRIX_1_LSB_ADDR         = 0X45
BNO055_SIC_MATRIX_1_MSB_ADDR         = 0X46
BNO055_SIC_MATRIX_2_LSB_ADDR         = 0X47
BNO055_SIC_MATRIX_2_MSB_ADDR         = 0X48
BNO055_SIC_MATRIX_3_LSB_ADDR         = 0X49
BNO055_SIC_MATRIX_3_MSB_ADDR         = 0X4A
BNO055_SIC_MATRIX_4_LSB_ADDR         = 0X4B
BNO055_SIC_MATRIX_4_MSB_ADDR         = 0X4C
BNO055_SIC_MATRIX_5_LSB_ADDR         = 0X4D
BNO055_SIC_MATRIX_5_MSB_ADDR         = 0X4E
BNO055_SIC_MATRIX_6_LSB_ADDR         = 0X4F
BNO055_SIC_MATRIX_6_MSB_ADDR         = 0X50
BNO055_SIC_MATRIX_7_LSB_ADDR         = 0X51
BNO055_SIC_MATRIX_7_MSB_ADDR         = 0X52
BNO055_SIC_MATRIX_8_LSB_ADDR         = 0X53
BNO055_SIC_MATRIX_8_MSB_ADDR         = 0X54

# Accelerometer Offset registers
ACCEL_OFFSET_X_LSB_ADDR              = 0X55
ACCEL_OFFSET_X_MSB_ADDR              = 0X56
ACCEL_OFFSET_Y_LSB_ADDR              = 0X57
ACCEL_OFFSET_Y_MSB_ADDR              = 0X58
ACCEL_OFFSET_Z_LSB_ADDR              = 0X59
ACCEL_OFFSET_Z_MSB_ADDR              = 0X5A

# Magnetometer Offset registers
MAG_OFFSET_X_LSB_ADDR                = 0X5B
MAG_OFFSET_X_MSB_ADDR                = 0X5C
MAG_OFFSET_Y_LSB_ADDR                = 0X5D
MAG_OFFSET_Y_MSB_ADDR                = 0X5E
MAG_OFFSET_Z_LSB_ADDR                = 0X5F
MAG_OFFSET_Z_MSB_ADDR                = 0X60

# Gyroscope Offset register s
GYRO_OFFSET_X_LSB_ADDR               = 0X61
GYRO_OFFSET_X_MSB_ADDR               = 0X62
GYRO_OFFSET_Y_LSB_ADDR               = 0X63
GYRO_OFFSET_Y_MSB_ADDR               = 0X64
GYRO_OFFSET_Z_LSB_ADDR               = 0X65
GYRO_OFFSET_Z_MSB_ADDR               = 0X66

# Radius registers
ACCEL_RADIUS_LSB_ADDR                = 0X67
ACCEL_RADIUS_MSB_ADDR                = 0X68
MAG_RADIUS_LSB_ADDR                  = 0X69
MAG_RADIUS_MSB_ADDR                  = 0X6A

# Power modes
POWER_MODE_NORMAL                    = 0X00
POWER_MODE_LOWPOWER                  = 0X01
POWER_MODE_SUSPEND                   = 0X02

# Operation mode settings
OPERATION_MODE_CONFIG                = 0X00
OPERATION_MODE_ACCONLY               = 0X01
OPERATION_MODE_MAGONLY               = 0X02
OPERATION_MODE_GYRONLY               = 0X03
OPERATION_MODE_ACCMAG                = 0X04
OPERATION_MODE_ACCGYRO               = 0X05
OPERATION_MODE_MAGGYRO               = 0X06
OPERATION_MODE_AMG                   = 0X07
OPERATION_MODE_IMUPLUS               = 0X08
OPERATION_MODE_COMPASS               = 0X09
OPERATION_MODE_M4G                   = 0X0A
OPERATION_MODE_NDOF_FMC_OFF          = 0X0B
OPERATION_MODE_NDOF                  = 0X0C

class BNO055:
    command_response_dict = {0x01: "WRITE_SUCCESS",
                            0x03: "WRITE_FAIL",
                            0x04: "REGMAP_INVALID_ADDRESS",
                            0x05: "REGMAP_WRITE_DISABLED",
                            0x06: "WRONG_START_BYTE",
                            0x07: "BUS_OVER_RUN_ERROR",
                            0X08: "MAX_LENGTH_ERROR",
                            0x09: "MIN_LENGTH_ERROR",
                            0x0A: "RECEIVE_CHARACTER_TIMEOUT"}

    read_response_dict = {0x02: "READ_FAIL",
                            0x04: "REGMAP_INVALID_ADDRESS",
                            0x05: "REGMAP_WRITE_DISABLED",
                            0x06: "WRONG_START_BYTE",
                            0x07: "BUS_OVER_RUN_ERROR",
                            0X08: "MAX_LENGTH_ERROR",
                            0x09: "MIN_LENGTH_ERROR",
                            0x0A: "RECEIVE_CHARACTER_TIMEOUT"}

    def __init__(self, uart_bus):
        self.uart = uart_bus
        self.uart.init(baudrate = 115200, parity= None, stop=1)

        self.write_register(BNO055_OPR_MODE_ADDR, OPERATION_MODE_CONFIG)

        self.write_register(BNO055_PWR_MODE_ADDR, POWER_MODE_NORMAL)

        self.write_register(BNO055_OPR_MODE_ADDR, OPERATION_MODE_NDOF)

        # store a set of last values in case a huge reading occurs
        # (as seen in testing) then the last value can be returned instead
        self.last_pitch = None
        self.last_roll = None
        self.last_yaw = None
        self.last_yaw_rate = None

        self.last_pitch = self.get_pitch()
        self.last_roll = self.get_roll()
        self.last_yaw = self.get_yaw()
        self.last_yaw_rate = self.get_yaw_rate()

    def write_register(self, register_adr, data):
        write_success = False
        tries = 0
        while (not write_success) and (tries < 20):
            command = bytearray([0xAA, 0x00, register_adr, 0x01, data])
            self.uart.write(command)
            # Found that a sleep of 10 ms helped the writes not fail...
            utime.sleep_ms(10)
            response = self.uart.readall()
            try:
                if response[1] == 0x01:
                    # print("Write to reg ", register_adr, " success!")
                    # print("Tries: ", tries)
                    write_success = True
                    break

            except TypeError:
                pass

            tries += 1

        if not write_success:
            print("BNO: Response for write to reg ", register_adr, " is : ", BNO055.command_response_dict[response[1]])
            print("BNO: Write to reg ", register_adr, " failed")

        return write_success

    def read_register(self, register_adr, num_bytes):
        read_success = False
        tries = 0
        while (not read_success) and (tries < 20):
            command = bytearray([0xAA, 0x01, register_adr, num_bytes])
            self.uart.write(command)
            utime.sleep_us(3500)
            response = self.uart.readall()
            try:
                if response[0] == 0xBB:
                    # print("Read from reg ", register_adr, " success!")
                    # print("Tries: ", tries)
                    read_success = True
                    break

            except TypeError:
                pass

            tries += 1

        if not read_success:
            print("BNO: Response for read from reg ", register_adr, " is : ", BNO055.read_response_dict[response[1]])
            print("BNO: Read from reg ", register_adr, " failed")

        return int.from_bytes(response[2:])

    def get_pitch(self):

        tempL = self.read_register(BNO055_EULER_P_LSB_ADDR, 1)
        tempH = self.read_register(BNO055_EULER_P_MSB_ADDR, 1)

        out = int((tempH << 8) | tempL) #bitshifting
        out = out/16 # divide all angles by 16 to get true angle in deg
        if out > 180:   #check if the value is overflowing
            out = out - 4095.9375

        # if still not between the -180, then return the last value
        if not -180<out<180:
            out = self.last_pitch

        self.last_pitch = out

        return out

    def get_roll(self):

        tempL = self.read_register(BNO055_EULER_R_LSB_ADDR, 1)
        tempH = self.read_register(BNO055_EULER_R_MSB_ADDR, 1)

        out = int((tempH << 8) | tempL) #bitshifting
        out = out/16 # divide all angles by 16 to get true angle in deg
        if out > 180:   #check if the value is overflowing
            out = out - 4095.9375

        # if still not between the -180, then return the last value
        if not -180 < out < 180:
            out = self.last_roll

        self.last_roll = out

        return out

    def get_yaw(self):

        tempL = self.read_register(BNO055_EULER_H_LSB_ADDR, 1)
        tempH = self.read_register(BNO055_EULER_H_MSB_ADDR, 1)

        out = int((tempH << 8) | tempL) #bitshifting
        out = out/16 # divide all angles by 16 to get true angle in deg
        if out > 180:   #check if the value is overflowing
            out = out - 4095.9375

        # if still not between the -180, then return the last value
        if not -180 < out < 180:
            out = self.last_yaw

        self.last_yaw = out

        return out

    def get_yaw_rate(self):

        tempL = self.read_register(BNO055_GYRO_DATA_Z_LSB_ADDR, 1)
        tempH = self.read_register(BNO055_GYRO_DATA_Z_MSB_ADDR, 1)

        out = int((tempH << 8) | tempL)  # bitshifting
        out = out / 16  # divide all angles by 16 to get true angle in deg
        if out > 360:  # check if the value is overflowing
            out = out - 4095.9375

        if out > 500:
            out = self.last_yaw_rate

        self.last_yaw_rate = out

        return out

    def deinit_uart(self):
        self.uart.deinit()

