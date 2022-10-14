plugins {
    id("application")
    kotlin("jvm") version "1.6.10"
}

repositories { mavenCentral() }
application { mainClass.set("MainKt") }

dependencies {
    implementation("__PACKAGE__") __IMPLEMENTATION_DETAILS__
}