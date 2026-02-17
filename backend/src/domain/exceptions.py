"""
Exceções do Domínio AlleFarma

Define exceções customizadas usadas nas camadas de domínio e aplicação.
"""


class ValidationError(Exception):
    """
    Erro de validação de domínio.

    Lançado quando dados violam regras de negócio.
    Diferente do ValueError — é específico do domínio AlleFarma!
    """

    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(message)

    def __str__(self):
        if self.field:
            return f"[{self.field}] {self.message}"
        return self.message


class MedicamentoNaoEncontradoError(Exception):
    """Lançado quando medicamento não é encontrado pelo ID."""

    def __init__(self, medicamento_id: int):
        self.medicamento_id = medicamento_id
        super().__init__(f"Medicamento com ID {medicamento_id} não encontrado")


class EstoqueInsuficienteError(Exception):
    """Lançado quando tentativa de remover mais estoque do que disponível."""

    def __init__(self, disponivel: int, solicitado: int):
        self.disponivel = disponivel
        self.solicitado = solicitado
        super().__init__(
            f"Estoque insuficiente: {disponivel} disponível, {solicitado} solicitado"
        )