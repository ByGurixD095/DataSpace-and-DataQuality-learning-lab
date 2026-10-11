// Proyecto Gradle del laboratorio 11-Eclipse-EDC.
// Estructura y módulos tomados de los Samples oficiales de EDC (Apache-2.0); ver NOTICE.md.
// A propósito NO se aplica el plugin "edc-build" de los Samples: añadiría comprobaciones de
// estilo (checkstyle y cabeceras de licencia) que no aportan nada a un laboratorio.

plugins {
    `java-library`
}

allprojects {
    group = "lab.espacio"
    version = "0.1.0"

    tasks.withType<JavaCompile>().configureEach {
        options.release.set(17)
    }
}
