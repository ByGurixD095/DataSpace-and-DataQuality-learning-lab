package lab.espacio.policy;

import org.eclipse.edc.participantcontext.spi.config.ParticipantContextConfig;
import org.eclipse.edc.runtime.metamodel.annotation.Inject;
import org.eclipse.edc.runtime.metamodel.annotation.Provider;
import org.eclipse.edc.spi.iam.AudienceResolver;
import org.eclipse.edc.spi.iam.ClaimToken;
import org.eclipse.edc.spi.iam.IdentityService;
import org.eclipse.edc.spi.iam.TokenParameters;
import org.eclipse.edc.spi.iam.TokenRepresentation;
import org.eclipse.edc.spi.iam.VerificationContext;
import org.eclipse.edc.spi.result.Result;
import org.eclipse.edc.spi.system.ServiceExtension;
import org.eclipse.edc.spi.types.TypeManager;

import java.util.Map;

/**
 * IDENTIDAD SIMULADA con una reclamación propia: "tipoParticipante" (ayuntamiento, universidad, startup).
 *
 * Basado en IamClaimsExtension de policy-01 de eclipse-edc/Samples, que hace lo mismo con "region".
 * El "token" no está firmado: cualquiera puede afirmar lo que quiera. Es la versión de juguete de lo que en
 * 06-Identidad-con-MVD se sustituye por credenciales verificables (DCP + Identity Hub).
 * La reclamación se configura con la propiedad edc.lab.tipo.participante.
 */
public class IamClaimsExtension implements ServiceExtension {

    public static final String CLAIM_TIPO = "tipoParticipante";
    private static final String SETTING_TIPO = "edc.lab.tipo.participante";

    @Inject
    private ParticipantContextConfig contextConfig;
    @Inject
    private TypeManager typeManager;
    @Inject
    private AudienceResolver audienceResolver; // necesario para poder sustituir el IdentityService de iam-mock

    @Override
    public String name() {
        return "Laboratorio: identidad simulada con tipoParticipante";
    }

    @Provider
    public IdentityService identityService() {
        return new MockClaimsIdentityService(contextConfig, typeManager);
    }

    private static class MockClaimsIdentityService implements IdentityService {
        private final ParticipantContextConfig contextConfig;
        private final TypeManager typeManager;

        MockClaimsIdentityService(ParticipantContextConfig contextConfig, TypeManager typeManager) {
            this.contextConfig = contextConfig;
            this.typeManager = typeManager;
        }

        @Override
        public Result<TokenRepresentation> obtainClientCredentials(String participantContextId, TokenParameters parameters) {
            var clientId = contextConfig.getString(participantContextId, "edc.participant.id");
            var token = Map.of(
                    "client_id", clientId,
                    CLAIM_TIPO, contextConfig.getString(participantContextId, SETTING_TIPO, "")
            );
            var tokenRepresentation = TokenRepresentation.Builder.newInstance()
                    .token(typeManager.writeValueAsString(token))
                    .build();
            return Result.success(tokenRepresentation);
        }

        @Override
        public Result<ClaimToken> verifyJwtToken(String participantContextId, TokenRepresentation tokenRepresentation, VerificationContext context) {
            Map<String, Object> token = typeManager.readValue(tokenRepresentation.getToken(), Map.class);

            return Result.success(ClaimToken.Builder.newInstance()
                    .claim("client_id", token.get("client_id"))
                    .claim(CLAIM_TIPO, token.get(CLAIM_TIPO))
                    .build());
        }
    }
}
