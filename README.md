# syntacore_it

## Тестовое задание на должность RTL Verificator Intern

1. Необходимо проверить операции ADD и SUB в SRC1 iALU (асинхронный интерфейс Main adder). На выходе ожидается:
- Test bench с набором тестов
- Покрытие кода
- Waveform
### Для запуска:
```
git clone git@github.com:yuegeini/syntacore_it.git
cd syntacore_it
make
```
#### Предварительно, необходимо, чтобы было установаены:
- cocotb
- verilator (Изменить в Makefile VERILATOR_ROOT)
- lcov
- gtkwave


### Результатом будtт:
- [testbench](./test_scr1_pipe_ialu.py)
- [html-отчет по покрытию](./logs/html/index.html)
- [waveform](./dump.vcd)
