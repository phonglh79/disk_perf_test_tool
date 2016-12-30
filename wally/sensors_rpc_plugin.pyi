from typing import NamedTuple, TypeVar, Callable, Any, Optional, List, Iterable, Dict, Tuple

Pid = TypeVar('Pid', str)
AnyFunc = TypeVar('AnyFunc', Callable[..., Any])
PrefixList = Optional[List[str]]
SensorDict = Dict[str, int]

def provides(name: str) -> Callable[[AnyFunc], AnyFunc]: ...
def is_dev_accepted(name: str, disallowed_prefixes: PrefixList, allowed_prefixes: PrefixList) -> bool: ...
def get_pid_name(pid: Pid) -> str: ...
def pid_stat(pid: Pid) -> float: ...
def get_mem_stats(pid : Pid) -> Tuple[int, int]: ...
def get_ram_size() -> int: ...

def io_stat(disallowed_prefixes: PrefixList, allowed_prefixes: PrefixList) -> int: ...
def net_stat(disallowed_prefixes: PrefixList, allowed_prefixes: PrefixList) -> int: ...
def pscpu_stat(disallowed_prefixes: PrefixList, allowed_prefixes: PrefixList) -> int: ...
def psram_stat(disallowed_prefixes: PrefixList, allowed_prefixes: PrefixList) -> int: ...
def syscpu_stat(disallowed_prefixes: PrefixList, allowed_prefixes: PrefixList) -> int: ...
def sysram_stat(disallowed_prefixes: PrefixList, allowed_prefixes: PrefixList) -> int: ...

