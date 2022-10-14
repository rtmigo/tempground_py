import os
import unittest
from pathlib import Path

from tempground import TempGround


class TestKotlin(unittest.TestCase):
    # will fail if gradle is not installed

    def test_app2(self):
        gradle_parent = Path(__file__).parent/"data"/"gradle"
        gradle_exe = gradle_parent / \
                     ("gradlew.bat" if os.name == "nt" else "gradlew")
        assert gradle_exe.exists()

        with TempGround(
                files={
                    "build.gradle.kts": """
                        plugins {
                            id("application")
                            kotlin("jvm") version "1.6.10"
                        }
                        
                        repositories { mavenCentral() }
                        application { mainClass.set("MainKt") }
                        
                        dependencies {
                            implementation("io.github.rtmigo:kitestsample")
                        }            
                    """,

                    "settings.gradle.kts": """
                        sourceControl {
                            gitRepository(java.net.URI("https://github.com/rtmigo/kitest_sample_kotlin_lib_kt.git")) {
                                producesModule("io.github.rtmigo:kitestsample")
                            }
                        }            
                    """,

                    "src/main/kotlin/Main.kt": """
                        import io.github.rtmigo.kitestsample.*
                        fun main() = println(greet())
                    """}) as app:
            # warm up gradle, so next time we'll get clean output
            app.run([gradle_exe, "help"])
            # run
            result = app.run([gradle_exe, "run", "-q", "--no-daemon"])

        self.assertEqual(result.stdout, "hello :)\n")
