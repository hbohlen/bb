"""Prove measure-s26.py's coarse-pointer guard fires.

Runs the measurement with the Emulation calls removed, which is exactly the
mistake the two earlier passes made, and asserts the script aborts instead of
reporting desktop sizes as phone sizes.

Run: python docs/design/scripts/check-coarse-guard.py
"""

import pathlib
import types


def main() -> None:
    src = pathlib.Path(__file__).with_name("measure-s26.py").read_text()
    mutated = src.replace('cdp.send("Emulation.setDeviceMetricsOverride", DEVICE)', "")
    mutated = mutated.replace(
        'cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})',
        "",
    )
    assert 'cdp.send("Emulation.setDeviceMetricsOverride"' not in mutated
    assert 'cdp.send("Emulation.setTouchEmulationEnabled"' not in mutated

    module = types.ModuleType("measure_without_emulation")
    module.__file__ = "measure-s26.py"
    exec(compile(mutated, "measure-s26.py", "exec"), module.__dict__)  # noqa: S102

    try:
        module.main()
    except SystemExit as exc:
        print(f"guard fired: {exc}")
        return
    raise SystemExit("guard did not fire; the script reported a measurement "
                     "taken without coarse-pointer emulation")


if __name__ == "__main__":
    main()