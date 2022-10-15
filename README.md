![Generic badge](https://img.shields.io/badge/python-3.10+-blue.svg)
![Generic badge](https://img.shields.io/badge/os-Linux_|_MacOS_|_Windows-blue.svg)


# [tempground](https://github.com/rtmigo/tempground_py)

A script that allows you to concisely:

* create a temp directory
* fill the directory with files of known content
* run shell commands in the directory
* check the run results

For example, during integration testing of a library, we can create a small temporary project that imports our library. And we check that the library was imported. 


### Example: Testing a Kotlin library

Suppose you have created a Kotlin library named `mylib`. You need to test that 
third-party projects can use `mylib` as a dependency.

The test can be run by creating a single file like this:

```python3
# lib_test.py

from tempground import *

with TempGround(
        files={
            # minimalistic build script to use the library
            "build.gradle.kts": """
                plugins {
                    id("application")
                    kotlin("jvm") version "1.6.10"
                }
                
                repositories { mavenCentral() }
                application { mainClass.set("MainKt") }
                
                dependencies {
                    implementation("io.github.username:mylib")
                }            
            """,

            # additional settings, if necessary 
            "settings.gradle.kts": """
                sourceControl {
                    gitRepository(java.net.URI("https://github.com/username/mylib.git")) {
                        producesModule("io.github.username:mylib")
                    }
                }            
            """,

            # kotlin code that imports and uses the library
            "src/main/kotlin/Main.kt": """
                import io.github.username:mylib.spanishGreeting
                fun main() = println(spanishGreeting())
            """}) as app:
    
    # print report about our mini-project
    print(app.files_content())
    
    # run our mini-project
    result = app.run(["gradle", "run", "-q"])
    
    # print what was on stdout, the exit code, etc 
    print(result)
    
    # check everything was as excepted
    assert result.returncode == 0
    assert result.stdout == "¡Hola!\n"

print("Everything is OK!")
```

To run the test on a clean system, install `tempground` and run the script:

```bash
# assuming pip and python are Python 3.10+
# and lib_test.py is a local file

$ pip install tempground
$ python lib_test.py
```

## License

Copyright © 2022 [Artsiom iG](https://github.com/rtmigo).
Released under the [MIT License](LICENSE).