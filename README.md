# LLMs in compiler domain

The broader compiler domain handles everything related to code, but has a specific goal on the translation and optimization aspects of code.

This repository surves as a survey of LLM Compiler related acedemic work. And will update subsequently.

A survey paper based on the following methodology will come up soon.

## Methodology

We can categorize LLM-Compiler researches in different ways.

### Way1: task about

1. translator (from A to B)
2. optimizer (from A to A)
3. bugfix (from a broken A to A)
4. generator (from NL to A, crossref to SE domain)

### Way2: code levels

1. source code
2. IR format
3. assembly/binary code
4. HDL/HLS
5. others

### Way3: contributions

1. new model
2. new workflow/agent
3. new dataset/benchmark
4. new approach on a specific task

### Way4: advancements

1. know cans and cants
2. less laber-intensive way
3. better optimization
4. broader applicability

## Finalized Categories

- Tasks: Transpilation(Compilation is its subset), Optimization, Bugfix
- Code levels: including NL, high-level PL, low-level assembly/IR/binary
- Combining Task and Code Level: there can be subtasks like: 
    1. compile/decompile/binary translation/source code transpilation(**transpilation**)
    2. source code optimization/IR-ASM optimization(**optimization**, including specific optimization like regalloc, etc.)
- Design ways: selector, code transformer(transform the code) or transform coder(code the transform)
- Scope: Inner-Compiler or Outer-Compiler
- Advancement:
    1. Know/Extend LLM's cans and cants
    2. Better optimization
    3. Broader utility
    4. Faster Implementation
    5. LLM-specific: like scalability and reliability

## Contact

This survey is lead by SKLP, ICT, CAS.
