// Runtime del conector del laboratorio. El MISMO jar sirve para el proveedor y para los consumidores:
// lo que cambia es el fichero de configuración (config/*.properties).
// Basado en transfer-00-prerequisites + policy-01 de eclipse-edc/Samples (EDC 0.18.1).

plugins {
    `java-library`
    id("application")
    alias(libs.plugins.shadow)
}

dependencies {
    runtimeOnly(libs.edc.bom.controlplane.base) {
        exclude(group = "org.eclipse.edc", module = "data-plane-signaling-core")
        exclude(group = "org.eclipse.edc", module = "data-plane-signaling-oauth2")
    }
    implementation(libs.edc.control.plane.api.client)
    implementation(libs.edc.iam.mock)                       // identidad simulada (se sustituye por DCP en 06)
    implementation(libs.edc.transfer.data.plane.signaling)
    implementation(libs.edc.validator.data.address.http.data)

    implementation(libs.edc.edr.cache.api)
    implementation(libs.edc.edr.store.core)
    implementation(libs.edc.edr.store.receiver)

    implementation(libs.edc.data.plane.self.registration)
    implementation(libs.edc.data.plane.signaling.api)
    implementation(libs.edc.data.plane.signaling.client)
    implementation(libs.edc.data.plane.core)
    implementation(libs.edc.data.plane.http)
    implementation(libs.edc.data.plane.iam)

    // Para la extensión de política propia (como policy-functions de los Samples)
    api(libs.edc.data.plane.spi)
    api(libs.edc.json.ld.spi)
    api(libs.edc.participant.context.config.spi)
    implementation(libs.edc.control.plane.core)
}

application {
    mainClass.set("org.eclipse.edc.boot.system.runtime.BaseRuntime")
}

var distTar = tasks.getByName("distTar")
var distZip = tasks.getByName("distZip")

tasks.shadowJar {
    mergeServiceFiles()
    archiveFileName.set("connector.jar")
    dependsOn(distTar, distZip)
    duplicatesStrategy = DuplicatesStrategy.INCLUDE
}
