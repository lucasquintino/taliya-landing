import type { Metadata } from "next";
import Link from "next/link";
import { legalDocuments } from "@/lib/legal/documents";

export const metadata: Metadata = {
  title: "Termos de Uso | Taliya",
  description: "Condições de acesso, assinatura e uso do aplicativo Taliya e dos recursos de inteligência artificial.",
  alternates: { canonical: "/termos" },
};

const sections = [
  {
    title: "1. Sobre a Taliya e estes Termos",
    paragraphs: [
      "A Taliya é uma ferramenta para apoiar o dono de um negócio de serviços na organização de clientes, serviços, agenda, pagamentos e documentos, conforme os recursos disponíveis em sua conta. Estes Termos regulam o acesso e o uso do aplicativo e complementam as condições da oferta apresentada na contratação.",
      "O serviço é fornecido por Taliya Inova Simples (I.S.), CNPJ 69.584.998/0001-15, com endereço na Rua Maria de Oliveira Mares Guia, 44, Praia de Itaparica, Vila Velha, ES, CEP 29102-245. Para atendimento, utilize contato@taliya.com.br. As condições comerciais são apresentadas antes da contratação e de qualquer pagamento.",
      "O cadastro deve ser realizado por pessoa maior de dezoito anos, com capacidade para contratar e autorização para representar o negócio informado. A contratação não depende de conversar com a inteligência artificial.",
    ],
  },
  {
    title: "2. Conta, acesso e segurança",
    paragraphs: [
      "Informe dados corretos e mantenha seus canais de acesso atualizados. Proteja os códigos de autenticação e não os compartilhe com terceiros. Avise o suporte se identificar acesso não autorizado. A Taliya não solicita senhas, códigos de acesso ou chaves de API pelo chat de atendimento.",
      "Utilize somente contas e dados para os quais você tenha autorização. Não tente acessar dados de outros negócios, contornar controles de segurança, introduzir arquivos maliciosos ou usar o serviço para atividades ilegais. Medidas de proteção podem restringir acessos suspeitos; conteste eventuais erros pelo contato de suporte.",
    ],
  },
  {
    title: "3. Assinatura, cobrança e cancelamento",
    paragraphs: [
      "Antes de contratar, confira o preço total, a periodicidade, a recorrência, os recursos incluídos e a forma de pagamento apresentados no checkout. O valor não é definido pela conversa com a IA. A assinatura é paga desde o início; a garantia não é um período de teste gratuito.",
      "A oferta da Taliya prevê garantia de reembolso de quatorze dias a partir da contratação inicial. Para solicitá-la, utilize contato@taliya.com.br e informe a conta e a contratação. Essa garantia não reduz os direitos assegurados pela legislação aplicável. Pedido recebido e reembolso concluído são estados diferentes; a conclusão depende da confirmação do meio de pagamento.",
      "Você pode solicitar o cancelamento da renovação pelo canal de gestão indicado na contratação ou pelo suporte. O cancelamento da renovação não equivale a excluir a conta, nem confirma automaticamente um reembolso. Acesso e cobranças seguem os fatos confirmados da assinatura e os direitos aplicáveis. Nenhum retorno de navegador ou mensagem da IA, isoladamente, comprova pagamento.",
    ],
  },
  {
    title: "4. Seus dados e os dados de seus clientes",
    paragraphs: [
      "Você mantém a titularidade sobre o conteúdo que registra e deve ter autorização ou outra base legal adequada para tratar os dados de seus clientes. Informe apenas o necessário à sua atividade, especialmente em documentos que contenham dados sensíveis. Você autoriza o processamento necessário à prestação das funções solicitadas, nos limites descritos na Política de Privacidade e na legislação aplicável.",
      "Aceitar estes documentos não representa autorização genérica para qualquer uso de dados, publicidade ou tratamento por IA. Autorizações específicas, quando exigidas, são tratadas separadamente e podem ser retiradas pelo canal disponibilizado. A finalidade e as condições do tratamento estão na Política de Privacidade.",
    ],
  },
  {
    title: "5. Inteligência artificial e operações",
    paragraphs: [
      "A Taliya utiliza serviços da OpenAI para interpretar pedidos, responder, preparar documentos e solicitar operações disponíveis no produto. Conforme o recurso e as permissões aplicáveis, mensagens, áudios, arquivos e informações necessárias do negócio podem ser enviados a esse fornecedor. O processamento depende das autorizações exigidas para a conta.",
      "A IA pode cometer erros, interpretar informações de forma incompleta ou produzir conteúdo impreciso. Confira os dados, valores e documentos antes de utilizá-los profissionalmente ou enviá-los a terceiros. Documentos e orientações não substituem a responsabilidade nem a avaliação do profissional habilitado, inclusive nas atividades regulamentadas.",
      "Pedidos claros podem executar operações autorizadas sem confirmação adicional em cada passo. Quando faltarem dados indispensáveis ou houver ambiguidade, a Taliya pode pedir esclarecimento. O resultado só deve ser considerado concluído quando houver confirmação do efeito salvo; em falhas ou resultado incerto, confira o registro antes de repetir uma operação financeira.",
      "No WhatsApp, o dono conversa com o número da Taliya para utilizar os recursos disponibilizados ao seu negócio. Isso não dá acesso às suas outras conversas pessoais nem autoriza a Taliya a conversar autonomamente com seus clientes.",
    ],
  },
  {
    title: "6. Documentos e arquivos",
    paragraphs: [
      "Conteúdos produzidos devem ser revisados pelo profissional responsável. Ao solicitar alterações, identifique o documento e o ajuste desejado. As possibilidades de criação, vinculação e histórico dependem dos recursos disponíveis no aplicativo. Respeite os direitos de terceiros sobre materiais enviados ou utilizados.",
      "Arquivos ficam em armazenamento privado. A Taliya mantém backup do banco de dados, sem backup adicional dos arquivos. Restaurar o banco não recupera arquivos definitivamente excluídos do armazenamento. Histórico válido não é apagado apenas por antiguidade para liberar espaço. Consulte a Política de Privacidade para os detalhes de armazenamento e retenção.",
    ],
  },
  {
    title: "7. Disponibilidade e suporte",
    paragraphs: [
      "O serviço depende de conexão e de fornecedores de infraestrutura, autenticação, IA e mensagens. Podem ocorrer manutenção, indisponibilidade e limitações técnicas. Metas internas de recuperação não constituem garantia de funcionamento ininterrupto ou prazo contratual de retorno. Informe falhas ao suporte para análise e recuperação.",
      "As responsabilidades da Taliya e seus direitos seguem a legislação aplicável. Estes Termos não excluem garantias legais, não afastam responsabilidades obrigatórias e não autorizam cobranças ou mudanças de plano sem a informação e a manifestação exigidas.",
    ],
  },
  {
    title: "8. Exclusão da conta e privacidade",
    paragraphs: [
      "A exclusão da conta e de seus dados pode ser solicitada pelos canais disponibilizados ou por contato@taliya.com.br, com confirmação da identidade. O processamento ocorre em até sete dias corridos, ressalvadas as obrigações legais de conservação informadas. Backups restritos do banco expiram em até trinta dias. Mensagens e arquivos já recebidos fora da Taliya não são apagados por essa solicitação.",
      "Excluir a conta e cancelar a renovação são providências distintas. Ao solicitar uma delas, informe também se deseja a outra para que o suporte confira a situação financeira e de acesso. A Política de Privacidade explica finalidades, fornecedores, retenção, direitos e canais para exercê-los.",
    ],
  },
  {
    title: "9. Versões, aceite e contato",
    paragraphs: [
      "No cadastro, você deve poder ler os documentos completos antes de confirmar o aceite. O registro deve identificar a conta, a data e as versões apresentadas. Abrir um link, entrar no aplicativo ou retornar do pagamento não substitui esse aceite. Alterações relevantes serão informadas e não modificam retroativamente o registro do que foi aceito.",
      "Para dúvidas, suporte, cancelamento, garantia ou questões de privacidade, utilize contato@taliya.com.br. Aplicam-se as leis brasileiras e são preservados os direitos e os meios de solução de conflitos assegurados pela legislação competente.",
    ],
  },
];

export default function TermsPage() {
  return (
    <main className="min-h-screen bg-[#F7F3EA] px-5 py-8 text-[#101B3A] sm:px-8 sm:py-12">
      <article className="mx-auto max-w-3xl">
        <Link className="inline-flex min-h-11 items-center font-bold text-[#0E8F7E] underline underline-offset-4" href="/">Voltar para a Taliya</Link>
        <header className="mt-6 rounded-lg border border-[#D8E6DC] bg-[#FFFDF8] p-5 sm:p-8">
          <h1 className="text-4xl font-black tracking-[-0.04em]">Termos de Uso</h1>
          <p className="mt-4 text-sm font-semibold text-[#667085]">Versão {legalDocuments.terms.version} · Atualização: 26 de outubro de 2026</p>
          <p className="mt-4 leading-7">Leia também a <Link className="font-bold text-[#0E8F7E] underline" href="/privacidade">Política de Privacidade</Link>, que detalha o tratamento de dados pessoais.</p>
        </header>
        <div className="mt-6 grid gap-6">
          {sections.map((section) => (
            <section className="rounded-lg border border-[#E6DCC8] bg-[#FFFDF8] p-5 sm:p-7" key={section.title}>
              <h2 className="text-2xl font-bold tracking-[-0.03em]">{section.title}</h2>
              <div className="mt-4 grid gap-4 text-base leading-7 text-[#344054]">{section.paragraphs.map((text) => <p key={text}>{text}</p>)}</div>
            </section>
          ))}
        </div>
      </article>
    </main>
  );
}
