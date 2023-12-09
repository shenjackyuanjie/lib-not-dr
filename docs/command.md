# Command parser

> By shenjackyuanjie And MSDNicrosoft and Harvey Huskey

## Usage

```python
from typing import Callable, Self, Optional, List

class Literal:
    def __init__(self, name: str):
        self.name = name
        self.sub = []
        self._tip = ''
    
    def __call__(self, *nodes) -> Self:
        self.sub += nodes
        return self
    
    def run(self, func: Callable[[List[str]], None]) -> Self:
        return self
    
    def tip(self, tip: str) -> Self:
        return self
    
    def arg(self, parse_func: Callable[[str], Optional[type]]) -> Self:
        return self
    
    def error(self, callback: Callable[[str], None]) -> Self:
        return self
    
    
builder = Literal('test1')(
    Literal('a')
        .run(lambda x: print(x)),
    Literal('b')
        .tip('this is b')
        .run(lambda x: print(x))(
            Literal('c')
                .run(lambda x: print(x)),
            Literal('d')
                .run(lambda x: print(x)),
        ),
    )
```

build

- test
- main
  - arg:text
    - go
  - arg:int
    - run

- command: 主节点
- literal: 字面量节点

## 设计思路

```rust
pub enum ArgumentType {
    String(String),
    Int(i128),
    Bool(bool),
    Float(f64),
}

pub type CallBackFunc = Fn(Vec<(String, ArgumentType)>) -> bool;

pub enum CallBack {
    Fn(CallBackFunc),
    Message(String),
}

pub trait Command {
    fn new(nodes: Vec<Command>) -> Self;
    // fn parse(&self, input: String) -> Result<Command, Error>;
    fn literal(&self, name: String, then: Vec<Command>) -> &self;
    fn argument(&self, name: String, shortcut: List<String>, optional: Option<bool>) -> &self;
    fn flag(&self, name: String, shortcut: List<String>, ) -> &self;
    fn error(&self, ret: CallBack) -> &self;
    fn run(&self, ret: CallBack) -> &self;
    fn tip(&self, tip: String) -> &self;
    fn to_doc(&self) -> String;
    fn exec(&self) -> Option;
}
```
