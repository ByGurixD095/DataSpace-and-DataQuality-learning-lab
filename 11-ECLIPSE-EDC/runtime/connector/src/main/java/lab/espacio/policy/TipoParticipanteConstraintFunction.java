package lab.espacio.policy;

import org.eclipse.edc.connector.controlplane.contract.spi.policy.ContractNegotiationPolicyContext;
import org.eclipse.edc.policy.engine.spi.AtomicConstraintRuleFunction;
import org.eclipse.edc.policy.model.Operator;
import org.eclipse.edc.policy.model.Permission;
import org.eclipse.edc.spi.monitor.Monitor;

import java.util.Objects;

import static java.lang.String.format;

/**
 * Evalúa la restricción "tipoParticipante" de una política ODRL durante la NEGOCIACIÓN:
 * compara el valor de la restricción con la reclamación "tipoParticipante" de quien pide el contrato.
 *
 * Es la versión real (en el conector) de lo que hacía evaluar_peticion() en 10-Data-Spaces.
 * Basado en LocationConstraintFunction de policy-01 de eclipse-edc/Samples.
 * Solo se admiten EQ y NEQ: cualquier otro operador DENIEGA (por defecto, lo no entendido no se concede).
 */
public class TipoParticipanteConstraintFunction implements AtomicConstraintRuleFunction<Permission, ContractNegotiationPolicyContext> {

    private final Monitor monitor;

    public TipoParticipanteConstraintFunction(Monitor monitor) {
        this.monitor = monitor;
    }

    @Override
    public boolean evaluate(Operator operator, Object rightValue, Permission rule, ContractNegotiationPolicyContext context) {
        var tipo = context.participantAgent().getClaims().get(IamClaimsExtension.CLAIM_TIPO);

        monitor.info(format("Evaluando restricción: tipoParticipante %s %s (solicitante: %s)", operator, rightValue, tipo));

        return switch (operator) {
            case EQ -> Objects.equals(tipo, rightValue);
            case NEQ -> !Objects.equals(tipo, rightValue);
            default -> false;
        };
    }
}
