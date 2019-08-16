import random
import cirq
import numpy as np

def U_f(qubits):
    '''
        Desc: There are four possible functions f
            1. f(x) = 0
            2. f(x) = 1
            3. f(0) = 0, f(1) = 1 (i.e f(x) = x)
            4. f(0) = 1, f(1) = 0 (i.e f(x) = ~x)
            And the quantum oracle U_f can be implemented by quantum gates, that is:
            
            1. Do nothing
                |x> ------- |x> 
                        
                |y> ------- |y ^ f(x)> == |y>

            2. NOT(y) 
                |x> ------- |x>
                |y> ------- |y ^ f(x)> == |y ^ 1> == |~y>

                i.e. 
                |00> -> |01>
                |01> -> |00>
                |10> -> |11>
                |11> -> |10>

            3. CNOT(x, y)
                |x> ------- |x>
                |y> ------- |y ^ f(x)> == |y ^ x>
                
                i.e.
                |00> -> |00>
                |01> -> |01>
                |10> -> |11>
                |11> -> |10>

            4. Apply gate X to |x> and apply CNOT(x, y) and apply gate X
                |x> ------- |x>
                |y> ------- |y ^ f(x)> == |y ^ ~x>
                
                i.e.
                |00> -> |01>
                |01> -> |00>
                |10> -> |10>
                |11> -> |11>
                
    '''
    # random sample a function
    f_index = random.randint(1, 4) - 1
    quantum_oracle = [
            [], 
            cirq.X(qubits[1]), 
            cirq.CNOT(qubits[0], qubits[1]), 
            [cirq.X(qubits[0]), cirq.CNOT(qubits[0], qubits[1]), cirq.X(qubits[0])]
            ]

    return quantum_oracle[f_index], f_index


def main():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    quantum_oracle, f_index = U_f(qubits)
    
    # Prepare |0> and |1>
    circuit.append(cirq.X(qubits[1]))
    # H transform 
    circuit.append([cirq.H(qubits[0]), cirq.H(qubits[1])], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
    # U_f
    circuit.append(quantum_oracle)
    # H transform
    circuit.append(cirq.H(qubits[0]))
    # Measure the first qubit
    circuit.append(cirq.measure(qubits[0], key="result"))

    print(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    result = result.measurements["result"] # A numpy nd array

    if f_index < 2:
        print("Constant")
        # result should be all |0> (False)
        assert(False == np.all(result))
        
    else:
        print("Balanced")
        # result should be all |1> (True)
        assert(True== np.all(result))

if __name__ == "__main__":
    main()

