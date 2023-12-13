# fixer


Small Python script that will add in an extra output port to Logisim-Evolution generated top-level files.

This is done since all the logic is running on a generated clock-tree and sometimes it's necessary to probe the state of those clocks, or to use it to drive other components in sync with the logic.

## How to get started
1. Clone the repo
2. Export your Logisim-Evolution design as Verilog (VHDL is not supported!)
3. Run the ``fixer.py`` script, passing in the path to the top-most directory of your design as an argument

For example, if the design is called ``my_cool_logisim_circuit``, the folder structure would look something like this:

```
─ my_cool_logisim_circuit/
  └── main/
      ├── sandbox/
      ├── scripts/
      ├── ucf/
      ├── verilog/
      ├── vhdl/
      └── xdc/
```
To execute the ``fixer.py`` script, run ``fixer.py path/to/my_cool_logisim_circuit``