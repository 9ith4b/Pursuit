import logging

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.DEBUG)
info    = logging.info
debug   = logging.debug

class Array:
    def __init__(self, start, step):
        self.address = start
        self.step = step

    def step_one(self):
        self.address += self.step
        return self.address


class Pursuit:
    ''' 追击类 '''
    def __init__(self, arr1: Array, arr2: Array):
        if arr1.step == arr2.step:
            raise Exception('Step error, the steps of two arrays cannot be equal.')
        
        if (arr1.address > arr2.address and arr1.step > arr2.step) or \
           (arr1.address < arr2.address and arr1.step < arr2.step):
            raise Exception('An array with a small address must have a step greater than an array with a large address.')
        
        if arr1.step > arr2.step:
            self.faster, self.slower = arr1, arr2
        else:
            self.faster, self.slower = arr2, arr1

        self.enter = 0      # 相遇点
        self.overlap = 0    # 重叠点
        self.leave = 0      # 分离点
    
    def enter_point(self):
        ''' 二者相遇的点，即将要发生数据覆盖的点 '''
        if self.faster.address >= self.slower.address:
            return self.enter
        
        self.faster.step_one()
        self.slower.step_one()
        self.enter += 1

        return self.enter_point()

    def overlap_point(self):
        ''' 二者重叠的点，即会覆盖彼此数据的点 '''
        if self.faster.address - self.slower.address >= self.slower.step:
            return self.enter+self.overlap
        
        self.faster.step_one()
        self.slower.step_one()
        self.overlap += 1

        return self.overlap_point()
    
    def leave_point(self):
        ''' 二者离开的点，即不会覆盖彼此数据的点 '''
        if self.faster.address - self.slower.address >= self.faster.step:
            return self.enter+self.overlap+self.leave
        
        self.faster.step_one()
        self.slower.step_one()
        self.leave += 1

        return self.leave_point()
    
    def get_points(self):
        enter = self.enter_point()
        overlap = self.overlap_point()
        leave = self.leave_point()
        info('Two arrays meet when index is %d' % enter)
        info('Two arrays are overlap each other when the index is %d' % overlap)
        info('Two arrays are far from each other when the index is %d' % leave)


if __name__ == '__main__':
    slower = Array(0x06020E0, 4)
    faster = Array(0x06020A0, 8)

    p = Pursuit(slower, faster)
    p.get_points()
