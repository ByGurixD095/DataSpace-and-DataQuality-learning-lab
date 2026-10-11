package lab.espacio.runtime;

import org.eclipse.edc.runtime.metamodel.annotation.Inject;
import org.eclipse.edc.spi.security.Vault;
import org.eclipse.edc.spi.system.ServiceExtension;
import org.eclipse.edc.spi.system.ServiceExtensionContext;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Carga en el vault EN MEMORIA el par de claves con el que el data plane firma y verifica los tokens
 * de acceso (las EDR del flujo "consumer pull").
 *
 * Basado en SeedVaultExtension de eclipse-edc/Samples, con una diferencia: los Samples llevan una clave
 * privada escrita en el código (válida solo para ejemplos). Aquí las claves se GENERAN con
 * 01-Entorno/generar-claves.sh y se leen de un directorio (variable LAB_KEYS_DIR, por defecto /keys).
 *
 * Solo para aprender: en un despliegue real se usa un vault de verdad.
 */
public class SeedVaultExtension implements ServiceExtension {

    @Inject
    private Vault vault;

    @Override
    public String name() {
        return "Laboratorio: carga de claves en el vault";
    }

    @Override
    public void initialize(ServiceExtensionContext context) {
        var dir = Path.of(System.getenv().getOrDefault("LAB_KEYS_DIR", "/keys"));
        vault.storeSecret("public-key", leer(dir.resolve("cert.pem")));
        vault.storeSecret("private-key", leer(dir.resolve("private.pem")));
        context.getMonitor().info("Claves cargadas desde " + dir);
    }

    private String leer(Path fichero) {
        try {
            return Files.readString(fichero);
        } catch (IOException e) {
            throw new UncheckedIOException("No se puede leer " + fichero + " (¿has ejecutado generar-claves.sh?)", e);
        }
    }
}
