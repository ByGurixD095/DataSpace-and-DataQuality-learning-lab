// Runtime del PROVEEDOR: el conector base + un proxy HTTP de data plane para el flujo "consumer pull".
// EDC no incluye un proxy listo para usar; este es el de transfer-03-consumer-pull de los Samples
// (solo GET, SOLO PARA APRENDER: en producción se usa un proxy de verdad).

plugins {
    `java-library`
    id("application")
    alias(libs.plugins.shadow)
}

dependencies {
    implementation(libs.edc.data.plane.spi)
    implementation(libs.edc.web.spi)
    implementation(libs.jakarta.rsApi)

    runtimeOnly(project(":runtime:connector"))
}

application {
    mainClass.set("org.eclipse.edc.boot.system.runtime.BaseRuntime")
}

var distTar = tasks.getByName("distTar")
var distZip = tasks.getByName("distZip")

tasks.withType<CreateStartScripts> {
    dependsOn(":runtime:connector:shadowJar")
}

tasks.shadowJar {
    mergeServiceFiles()
    archiveFileName.set("provider.jar")
    dependsOn(distTar, distZip)
    duplicatesStrategy = DuplicatesStrategy.INCLUDE
}
