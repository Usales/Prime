# 🤝 Contribuindo para o Prime

Obrigado por considerar contribuir para o Prime! Este é um projeto experimental e toda ajuda é bem-vinda.

## Como Contribuir

### 1. Reportar Bugs

Se encontrar um bug, por favor:

1. Verifique se o bug já foi reportado nas [Issues](https://github.com/Usales/Prime/issues)
2. Se não foi, crie uma nova issue com:
   - Descrição clara do bug
   - Passos para reproduzir
   - Comportamento esperado vs. atual
   - Informações do ambiente (OS, Python, etc.)

### 2. Sugerir Melhorias

1. Verifique se a sugestão já existe nas [Issues](https://github.com/Usales/Prime/issues)
2. Crie uma nova issue descrevendo:
   - O problema que a melhoria resolveria
   - Sua proposta de solução
   - Exemplos de uso, se aplicável

### 3. Contribuir com Código

#### Fork e Clone

```bash
# Faça fork do repositório no GitHub
# Clone seu fork
git clone https://github.com/SEU_USUARIO/Prime.git
cd Prime
```

#### Ambiente de Desenvolvimento

```bash
# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt
```

#### Padrões de Código

- Use Python 3.10+
- Siga PEP 8
- Adicione docstrings para funções e classes
- Escreva comentários explicativos quando necessário

#### Commits

- Use mensagens de commit claras e descritivas
- Formato: `tipo: descrição`
- Tipos comuns: `feat`, `fix`, `docs`, `refactor`, `test`

Exemplos:
```
feat: adicionar novo sistema de memória de longo prazo
fix: corrigir erro na inicialização do sistema sensorial
docs: atualizar README com novas instruções
```

### 4. Pull Requests

1. Crie uma branch para sua feature/fix:
   ```bash
   git checkout -b minha-feature
   ```

2. Faça suas alterações

3. Commit suas mudanças:
   ```bash
   git add .
   git commit -m "feat: descrição da mudança"
   ```

4. Push para seu fork:
   ```bash
   git push origin minha-feature
   ```

5. Abra um Pull Request no GitHub

## Diretrizes

### Arquitetura

- O Prime é composto por 7 sistemas independentes
- Cada sistema deve ser autônomo
- Comunicação entre sistemas via eventos ou estados compartilhados

### Princípios

- **LLM nunca decide** - O LLM apenas verbaliza decisões
- **Imperfeição controlada** - Erros propositais são válidos
- **Memória afetiva** - Lembrar com peso emocional

### Testes

- Adicione testes quando possível
- Teste casos de borda
- Documente comportamento esperado

## Perguntas?

Se tiver dúvidas, abra uma issue ou entre em contato.

Obrigado por contribuir! 🎉
