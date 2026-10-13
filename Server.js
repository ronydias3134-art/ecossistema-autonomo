// ==========================================
// ECOSSISTEMA AUTÓNOMO - MOTOR DE MARGENS
// Atualização: Piso de 10% (Zero Tolerância)
// ==========================================

const CONFIG = {
    MARGEM_EXCELENCIA: 0.40, // >= 40% (Excelência / Prioridade Máxima)
    MARGEM_PADRAO: 0.20,     // 20% a 39.9% (Aval Padrão)
    MARGEM_PISO: 0.10        // 10% a 19.9% (Aval Rígido - Novo Piso)
};

function avaliarOportunidade(precoCusto, precoVenda) {
    const lucroBruto = precoVenda - precoCusto;
    const margemPercentual = lucroBruto / precoCusto;

    // 1. Rejeição Automática (Abaixo de 10%)
    if (margemPercentual < CONFIG.MARGEM_PISO) {
        return { 
            estado: 'REJEITADO', 
            motivo: 'Margem inferior ao piso de 10%' 
        };
    }

    // 2. Zona Rígida (10% a 19.9%) - Requer Aprovação Humana Estrita
    if (margemPercentual >= CONFIG.MARGEM_PISO && margemPercentual < CONFIG.MARGEM_PADRAO) {
        return { 
            estado: 'PENDENTE_APROVACAO_HUMANA', 
            prioridade: 'MEDIA', 
            alerta: 'Zona de Aval Rígido (10%-19.9%)' 
        };
    }

    // 3. Zona Padrão (20% a 39.9%) - Aprovação Padrão
    if (margemPercentual >= CONFIG.MARGEM_PADRAO && margemPercentual < CONFIG.MARGEM_EXCELENCIA) {
        return { 
            estado: 'PENDENTE_APROVACAO_HUMANA', 
            prioridade: 'ALTA',
            alerta: 'Zona Padrão (20%-39.9%)'
        };
    }

    // 4. Excelência (40% ou mais) - Prioridade Máxima
    return { 
        estado: 'EXCELENCIA', 
        prioridade: 'MAXIMA',
        alerta: 'Margem de Excelência (>= 40%)' 
    };
}

module.exports = { avaliarOportunidade, CONFIG };
