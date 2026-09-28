import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Política de privacidade | Taliya",
  description:
    "Saiba como a Taliya trata dados pessoais no site, no assistente de IA e nos canais de atendimento comercial.",
  robots: {
    index: true,
    follow: true,
  },
};

const privacyEmail = "contato@taliya.com.br";

const tableOfContents = [
  ["resumo", "Resumo"],
  ["escopo", "Escopo deste aviso"],
  ["dados", "Dados que usamos"],
  ["uso", "Como usamos"],
  ["ia-whatsapp", "IA e WhatsApp"],
  ["compartilhamento", "Compartilhamento e fornecedores"],
  ["retencao", "Retenção"],
  ["direitos", "Seus direitos"],
  ["contato", "Contato"],
] as const;

const summaryItems = [
  "Usamos dados de contato e informações que você compartilha para responder dúvidas e dar continuidade ao atendimento solicitado.",
  "Mensagens e dados relevantes da conversa podem ser processados pela IA usada pela Taliya e registrados para manter o atendimento.",
  "No WhatsApp, a Meta processa telefone, mensagens e informações necessárias para entregar o serviço de mensagens.",
  "Você pode pedir acesso, correção ou exclusão de dados e solicitar que o contato seja interrompido pelo canal desta página.",
];

const dataItems = [
  "Nome, email, telefone ou número do WhatsApp, quando você os informa.",
  "Nome e tipo do negócio, cidade ou estado e contexto que você compartilha sobre sua operação.",
  "Serviços, rotinas, dúvidas, interesses e próximos passos que você descreve.",
  "Mensagens trocadas com o assistente no site ou pelo WhatsApp e informações necessárias para manter o contexto da conversa.",
  "Identificadores de sessão e informações de origem, como página, seção, referência de acesso e parâmetros de campanha na URL.",
  "Interações com o assistente e solicitações de atendimento, inclusive registros necessários para encaminhar a conversa à equipe.",
];

const useItems = [
  "Responder às perguntas e aos pedidos que você inicia pelo site ou pelo WhatsApp.",
  "Entender o contexto informado para explicar a Taliya e sugerir um próximo passo relacionado à sua solicitação.",
  "Manter o contexto do atendimento e encaminhar a conversa a uma pessoa da equipe quando necessário.",
  "Registrar solicitações e interações comerciais na caixa de atendimento da Taliya.",
  "Entregar respostas pelo WhatsApp e respeitar pedidos para interromper mensagens.",
  "Manter, proteger e melhorar o funcionamento dos canais e cumprir obrigações legais aplicáveis.",
];

const rights = [
  "confirmar se tratamos seus dados e solicitar acesso a eles;",
  "pedir a correção de dados incompletos, inexatos ou desatualizados;",
  "pedir anonimização, bloqueio ou eliminação quando aplicável;",
  "solicitar informações sobre o compartilhamento dos seus dados;",
  "revogar consentimento ou se opor ao tratamento, quando aplicável;",
  "solicitar a revisão de decisões tomadas unicamente com base em tratamento automatizado, nos termos da lei.",
];

export default function PrivacyPage() {
  return (
    <main className="min-h-screen bg-[#F7F3EA] text-[#101B3A]">
      <article className="mx-auto grid max-w-6xl gap-8 px-5 py-8 sm:px-8 sm:py-12 lg:grid-cols-[15rem_minmax(0,1fr)] lg:px-12">
        <aside className="lg:sticky lg:top-8 lg:self-start">
          <a
            aria-label="Voltar para a página da Taliya"
            className="inline-flex h-11 w-11 items-center justify-center rounded-full border border-[#D8E6DC] bg-white text-xl font-black leading-none text-[#0E8F7E] transition hover:border-[#0E8F7E] hover:bg-[#F3FBF8] focus:outline-none focus:ring-4 focus:ring-[#0E8F7E]/18"
            href="/"
          >
            <span aria-hidden="true">←</span>
          </a>

          <nav aria-label="Índice da política de privacidade" className="mt-8 hidden border-l border-[#D8E6DC] pl-4 lg:block">
            <p className="text-xs font-black uppercase tracking-[0.16em] text-[#667085]">Nesta página</p>
            <div className="mt-3 grid gap-1">
              {tableOfContents.map(([href, label]) => (
                <a
                  className="rounded-md px-2 py-1.5 text-sm font-black leading-5 text-[#344054] transition hover:bg-white hover:text-[#0E8F7E] focus:outline-none focus:ring-4 focus:ring-[#0E8F7E]/16"
                  href={`#${href}`}
                  key={href}
                >
                  {label}
                </a>
              ))}
            </div>
          </nav>
        </aside>

        <div className="min-w-0">
          <section className="rounded-lg border border-[#D8E6DC] bg-[#FFFDF8] p-5 shadow-[0_18px_48px_rgba(16,27,58,0.06)] sm:p-8" id="resumo">
            <p className="text-xs font-black uppercase tracking-[0.18em] text-[#0E8F7E]">Privacidade</p>
            <h1 className="mt-3 max-w-3xl text-4xl font-black leading-[0.95] tracking-[-0.04em] sm:text-5xl">
              Política de privacidade
            </h1>
            <p className="mt-5 max-w-3xl text-base font-semibold leading-7 text-[#667085]">
              Esta página explica como a Taliya trata dados pessoais quando você acessa o site, conversa com o assistente
              ou solicita atendimento pelos canais comerciais.
            </p>
            <p className="mt-4 text-sm font-black text-[#344054]">Última atualização: 28 de setembro de 2026</p>

            <div className="mt-7 grid gap-3 sm:grid-cols-2">
              {summaryItems.map((item) => (
                <p className="rounded-lg bg-[#F3FBF8] p-4 text-sm font-bold leading-6 text-[#344054]" key={item}>
                  {item}
                </p>
              ))}
            </div>
          </section>

          <div className="mt-8 grid gap-6">
            <PolicySection id="escopo" title="Escopo deste aviso">
              <p>
                Este aviso cobre o site da Taliya, o assistente comercial, os formulários de interesse e o atendimento
                pelo WhatsApp. Ele trata das informações usadas para apresentar o serviço e responder às solicitações
                comerciais.
              </p>
              <p>
                As informações de clientes, serviços, agenda e recebimentos que uma pessoa usuária registra durante a
                operação do negócio têm finalidade diferente. Não envie dados pessoais de clientes nem informações
                sensíveis pelo assistente comercial.
              </p>
              <p>
                Para assuntos relacionados a estes canais, o contato de privacidade da Taliya é {privacyEmail}.
              </p>
            </PolicySection>

            <PolicySection id="dados" title="Dados que usamos">
              <p>
                Recebemos as informações que você escolhe compartilhar e alguns dados técnicos necessários para manter
                o atendimento e entender de onde veio uma solicitação:
              </p>
              <SimpleList items={dataItems} />
              <Notice>
                O assistente comercial não precisa de dados pessoais dos seus clientes, informações de saúde, senhas ou
                dados completos de pagamento. Evite enviar essas informações nas conversas.
              </Notice>
            </PolicySection>

            <PolicySection id="uso" title="Como usamos esses dados">
              <SimpleList items={useItems} />
              <p>
                A base legal depende do pedido e da finalidade. Pode incluir responder a uma solicitação e realizar
                procedimentos pré-contratuais, cumprir obrigações legais, proteger os canais ou obter consentimento
                quando ele for necessário. Quando o tratamento se apoiar em consentimento, você pode revogá-lo.
              </p>
            </PolicySection>

            <PolicySection id="ia-whatsapp" title="IA, chat e WhatsApp">
              <p>
                Para gerar respostas, o assistente pode enviar à OpenAI a mensagem que você escreveu, trechos recentes da
                conversa e informações de contexto relacionadas ao atendimento.
              </p>
              <p>
                Se você escolher continuar pelo WhatsApp, a Meta/WhatsApp processa o número, o conteúdo das mensagens e
                os dados necessários para encaminhar e informar o status de entrega. A conversa pode ser registrada nos
                sistemas de atendimento da Taliya para dar continuidade ao pedido.
              </p>
              <p>
                O assistente pode preparar uma recomendação ou encaminhar a conversa para a equipe. Você pode pedir a
                qualquer momento que a Taliya interrompa o contato pelo WhatsApp.
              </p>
            </PolicySection>

            <PolicySection id="compartilhamento" title="Compartilhamento e fornecedores">
              <p>
                Para prestar o atendimento, os dados podem ser tratados por fornecedores de IA, WhatsApp, hospedagem e
                banco de dados usados pela Taliya. Quando uma integração de automação estiver configurada, informações
                relacionadas ao pedido também podem ser encaminhadas por webhook para essa integração.
              </p>
              <p>
                Os dados encaminhados variam conforme a etapa do atendimento e a integração utilizada. Quando isso for
                necessário para cumprir a lei, responder a uma ordem válida, prevenir fraude ou proteger direitos,
                também podemos compartilhar informações com as autoridades competentes.
              </p>
            </PolicySection>

            <PolicySection id="retencao" title="Retenção e exclusão">
              <p>
                Os registros de leads e conversas podem permanecer na caixa interna de atendimento até que a equipe os
                exclua. Atualmente, eles não são apagados automaticamente após um número fixo de dias.
              </p>
              <p>
                Você pode solicitar a exclusão pelo contato de privacidade desta página. O pedido será analisado conforme
                a situação e os dados poderão ser mantidos quando houver obrigação legal ou necessidade de exercer
                direitos.
              </p>
            </PolicySection>

            <PolicySection id="direitos" title="Seus direitos">
              <p>Nos termos da LGPD, você pode solicitar:</p>
              <SimpleList items={rights} />
              <p>
                Para proteger sua privacidade, podemos pedir informações suficientes para confirmar sua identidade e
                localizar o registro.
              </p>
            </PolicySection>

            <PolicySection id="contato" title="Contato de privacidade">
              <p>
                Para exercer seus direitos, tirar dúvidas ou pedir a interrupção do contato, envie uma mensagem para{" "}
                <a
                  className="font-black text-[#0E8F7E] underline-offset-4 hover:underline focus:outline-none focus:ring-4 focus:ring-[#0E8F7E]/16"
                  href={`mailto:${privacyEmail}`}
                >
                  {privacyEmail}
                </a>
                .
              </p>
              <p>
                Se possível, informe o canal usado, o email ou WhatsApp relacionado à conversa e o tipo de pedido. Não
                envie documentos sensíveis sem necessidade.
              </p>
            </PolicySection>
          </div>
        </div>
      </article>
    </main>
  );
}

function PolicySection({ children, id, title }: { children: ReactNode; id: string; title: string }) {
  return (
    <section className="scroll-mt-8 rounded-lg border border-[#E6DCC8] bg-[#FFFDF8] p-5 sm:p-7" id={id}>
      <h2 className="text-2xl font-black tracking-[-0.03em] text-[#101B3A]">{title}</h2>
      <div className="mt-4 grid gap-4 text-base font-semibold leading-7 text-[#344054]">{children}</div>
    </section>
  );
}

function SimpleList({ items }: { items: string[] }) {
  return (
    <ul className="grid gap-2 text-sm leading-6 sm:grid-cols-2">
      {items.map((item) => (
        <li className="pl-4 font-bold text-[#344054] before:-ml-4 before:mr-2 before:text-[#0E8F7E] before:content-['•']" key={item}>
          {item}
        </li>
      ))}
    </ul>
  );
}

function Notice({ children }: { children: ReactNode }) {
  return (
    <div className="rounded-lg border border-[#D3A52D]/32 bg-[#FFF8E7] p-4 text-sm font-bold leading-6 text-[#5D4A16]">
      {children}
    </div>
  );
}
