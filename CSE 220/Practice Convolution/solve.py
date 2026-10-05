class DiscreteSignal:
    def __init__(self,start_time:int,end_time:int) :
        self.start_time=start_time
        self.end_time=end_time
        self.values={t: 0 for t in range(start_time,end_time+1)}
    def set_value_at_time(self,t:int,value:float):
        if t<self.start_time or t>self.end_time:
            raise IndexError("Wrong input")
        self.values[t]=value # type: ignore
    def get_value_at_time(self,t:int):
        return self.values.get(t,0)
    def shift(self,k:int):
        shifted=DiscreteSignal(self.start_time+k,self.end_time+k)
        for t,v in self.values.items():
            shifted.values[t+k]=v
        
        return shifted
    
    def __repr__(self) -> str:
        times = sorted(self.values)
        header = "n     " + "  ".join(f"{t:>4}" for t in times)
        row    = "x[n]  " + "  ".join(f"{self.values[t]:>4}" for t in times)
        return header + "\n" + row    
    
    
class LTISystem:
    def __init__(self,impulse_response:DiscreteSignal) :
        self.h=impulse_response
        
    def output(self,input_signal:DiscreteSignal):
        x=input_signal
        h=self.h
        
        output_start=x.start_time+h.start_time
        output_end=x.end_time+h.end_time
        
        
        y=DiscreteSignal(output_start,output_end)
        
        for n in range(output_start,output_end+1):
            total=0.0
            for k in range(x.start_time,x.end_time+1):
                total+=x.get_value_at_time(k)*h.get_value_at_time(n-k)
                        
            y.set_value_at_time(n,total)
                        
        return y
    
if __name__ == "__main__":
    # --- Problem 1 demo: shift ---
    print("=" * 40)
    print("Problem 1 — DiscreteSignal & shift()")
    print("=" * 40)
 
    x = DiscreteSignal(-1, 1)
    x.set_value_at_time(-1, 2)
    x.set_value_at_time(0,  1)
    x.set_value_at_time(1,  3)
 
    print("\nOriginal signal:")
    print(x)
 
    shifted = x.shift(2)
    print("\nAfter shift(2):")
    print(shifted)
 
    # --- Problem 2 demo: LTI convolution ---
    print("\n" + "=" * 40)
    print("Problem 2 — LTI System convolution")
    print("=" * 40)
 
    # Input signal x[n]: n = 0,1,2 → values 1,2,1
    x2 = DiscreteSignal(0, 2)
    x2.set_value_at_time(0, 1)
    x2.set_value_at_time(1, 2)
    x2.set_value_at_time(2, 1)
 
    # Impulse response h[n]: n = 0,1 → values 1,-1
    h = DiscreteSignal(0, 1)
    h.set_value_at_time(0,  1)
    h.set_value_at_time(1, -1)
 
    system = LTISystem(h)
    y = system.output(x2)
 
    print(f"\nOutput time range: [{y.start_time}, {y.end_time}]")
    print("\nOutput signal:")
    print(y)                    