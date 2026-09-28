# Autonomous WhatsApp Flow Map

**Feature**: Premium Multi-Niche Landing Page System  
**Niche**: Pilates  
**Purpose**: Define the 5 strongest WhatsApp-first automation flows to power landing mockups, phone screens, agent demos and future SaaS behavior.

## Autonomy Rule

These flows are designed as autonomous WhatsApp flows only when the studio has pre-approved the message rules, tone, schedule windows and allowed actions.

The agent can act alone for low-risk operational routines:

- answer common questions from configured business data;
- offer available time options;
- confirm presence;
- send reminders;
- organize make-up class options;
- send payment reminders or payment links already configured by the studio;
- mark outcomes in the operational panel.

The agent must pause or hand off when:

- the student mentions pain, injury, medical restrictions or emotional distress;
- the student asks for discounts, refunds, cancellation terms or exceptions;
- there is conflicting agenda/payment data;
- the requested action changes a sensitive business rule;
- confidence is low or the student is upset.

## Flow 1: Atendimento - First WhatsApp Triage To Trial Class Booked

**Landing job**: Show that messages do not sit in WhatsApp waiting for the reception desk.

**Autonomous outcome**: The agent answers the interested person, qualifies the basic need and books a trial class without human participation.

**Trigger**

- New WhatsApp message from a known or unknown contact.
- Example: "Oi, queria saber horarios e valores."

**Customer Action**

1. Interested person sends a WhatsApp message.
2. They ask about hours, plans, trial class, location or availability.
3. They choose a preferred schedule window.
4. They confirm the trial class option.
5. They receive address, preparation instructions and confirmation.

**AI Action**

1. Classifies intent: information request with trial-class potential.
2. Checks approved studio data: hours, plans, location, trial class rules, available channels.
3. Asks for preferred schedule window.
4. Checks available trial class slots.
5. Offers two compatible options.
6. Books the selected trial class.
7. Sends confirmation with address, arrival guidance and what to bring.
8. Adds the person to the interested-person list with source `WhatsApp`.
9. If the person asks for medical guidance, discounts or exceptions, pauses and creates a human review item.

**Phone Screen Action**

- Header: `Agente Atendimento`
- Status chip: `modo automatico`
- Message sequence:
  1. Interested person: "Oi, queria saber horarios e valores."
  2. Background process card: `Intencao detectada: horarios e valores`
  3. Background process card: `Consultando turmas, planos e regras de aula experimental`
  4. Agent: "Oi! Temos turmas de manha, tarde e noite. Voce quer conhecer com uma aula experimental?"
  5. Interested person: "Quero sim. Melhor depois das 18h."
  6. Background process card: `Buscando vagas apos 18h`
  7. Background process card: `2 opcoes compativeis encontradas`
  8. Agent: "Tenho quarta 18h30 ou quinta 19h. Qual fica melhor?"
  9. Interested person: "Quinta 19h."
  10. Background process card: `Reservando aula experimental`
  11. Agent: "Perfeito, deixei sua aula experimental reservada para quinta as 19h. Chegue 10 min antes e venha com roupa confortavel."
  12. Agent: "Endereco: Rua Exemplo, 123. Se precisar remarcar, pode me chamar por aqui."
  13. Responsible notification: "Nova aula experimental marcada: Julia, quinta as 19h. Origem: WhatsApp. Horario reservado no sistema."
- System card: `Aula experimental reservada`
- Bottom state: `Conversa resolvida sem acionar recepcao`

**Automation Steps For Mockup**

1. Incoming message appears.
2. Agent answer appears automatically.
3. Customer reply appears.
4. Two schedule options appear inside an agent bubble.
5. Customer chooses one option.
6. Confirmation bubble appears.
7. System card changes to `Aula experimental reservada`.

**Tools Needed Later**

- `whatsapp.read_message`
- `studio.get_public_info`
- `conversation.classify_intent`
- `schedule.find_trial_slots`
- `schedule.book_trial_class`
- `crm.create_interested_person`
- `whatsapp.send_message`
- `task.create_handoff`

**Terminal States**

- `trial_class_booked`
- `human_review_required`

## Flow 2: Agenda - Absence To Filled Slot And Make-Up Class Recorded

**Landing job**: Show that an absence can become an occupied slot before the class starts.

**Autonomous outcome**: The agent confirms the absence, records make-up class credit, fills the open slot and confirms the replacement student.

**Trigger**

- Student sends: "Hoje nao vou conseguir ir na aula das 19h."
- Or a scheduled confirmation receives "nao vou".

**Customer Action**

1. Original student says they cannot attend.
2. Agent confirms the absence and records a make-up class credit when rules allow it.
3. Another student receives an available slot invitation.
4. Replacement student accepts.
5. Both students receive clear confirmation.

**AI Action**

1. Detects absence/cancellation.
2. Finds class and time from the message context.
3. Checks whether the studio has make-up class rules enabled and whether the student's plan allows make-up credit.
4. Records credit for original student only when the studio uses make-up classes and the student is eligible.
5. Releases slot.
6. Finds compatible students with pending make-up class or matching schedule preference.
7. Sends a slot invitation to the best candidate.
8. Confirms the slot when the candidate accepts.
9. Sends confirmation to replacement student.
10. Updates original class occupancy and operational panel with recovered slot.
11. Hands off if the class has special restrictions or teacher review is required.

**Phone Screen Action**

- Header: `Agente Agenda`
- Status chip: `modo automatico`
- Message sequence:
  1. Student A: "Hoje nao vou conseguir ir na aula das 19h."
  2. Background process card: `Ausencia detectada: turma das 19h`
  3. Background process card: `Conferindo se o studio usa regra de reposicao`
  4. Agent: "Sem problema. Registrei sua ausencia e deixei 1 reposicao disponivel para voce usar dentro da regra do studio."
  5. Background process card: `Liberando vaga na turma`
  6. Background process card: `Procurando aluno com reposicao pendente e horario compativel`
  7. Background process card: `Carol encontrada como melhor encaixe`
  8. Agent to Student A: "Quando quiser usar sua reposicao, me chama por aqui que eu te mostro os melhores horarios."
  9. Conversation switch card: `Abrindo conversa com Carol`
  10. Agent to Student B: "Oi, Carol. Abriu uma vaga hoje as 19h na turma de aparelhos. Quer usar sua reposicao nesse horario?"
  11. Student B: "Quero sim."
  12. Background process card: `Confirmando reposicao e atualizando ocupacao da turma`
  13. Agent: "Combinado, sua reposicao ficou confirmada para hoje as 19h. Te esperamos."
  14. Responsible notification: "Vaga das 19h recuperada: ausencia registrada para Aluno A e reposicao confirmada para Carol."
- System cards:
  - `Vaga liberada: 19h`
  - `Reposicao da Carol confirmada`
- Bottom state: `Vaga recuperada antes da aula`

**Automation Steps For Mockup**

1. Absence bubble enters.
2. Agent confirms make-up credit in Student A conversation.
3. Agent closes Student A conversation.
4. Slot card appears.
5. Conversation switches to candidate.
6. Invitation message is sent.
7. Candidate accepts.
8. Confirmation appears.
9. Slot turns green and result appears.

**Tools Needed Later**

- `whatsapp.read_message`
- `schedule.find_class`
- `makeup.check_eligibility`
- `makeup.create_credit`
- `schedule.release_slot`
- `students.find_makeup_candidates`
- `whatsapp.send_message`
- `schedule.reserve_slot`
- `operations.log_recovered_slot`

**Terminal States**

- `slot_filled`
- `makeup_credit_created`
- `candidate_declined`
- `no_candidate_found`
- `human_review_required`

## Flow 3: Vendas - Trial Class To First Plan Reserved

**Landing job**: Show that interested people do not disappear after asking price or taking a trial class.

**Autonomous outcome**: The agent follows up after the trial class, answers plan questions from approved data and reserves the first fixed schedule.

**Trigger**

- Trial class marked as completed.
- Interested person asked for price and stopped answering.
- Interested person clicked a WhatsApp CTA and shared preferred time.

**Customer Action**

1. Interested person attends trial class.
2. They receive a friendly follow-up.
3. They ask about plans or schedule.
4. They choose a fixed time.
5. They send basic pre-enrollment data.
6. They receive a warm confirmation that the responsible person from the studio will finalize enrollment.

**AI Action**

1. Detects stage: asked price, booked trial, attended trial, no response after trial.
2. Uses context: name, class attended, teacher, preferred time and plan options.
3. Sends a personal message without pressure.
4. Answers approved plan/routine questions.
5. Checks available fixed schedules.
6. Offers two compatible options.
7. Asks for basic pre-enrollment data.
8. Creates a pre-enrollment record in the system.
9. Sends a warm confirmation that the responsible person from the studio will finalize enrollment.
10. If pricing exceptions, discounts, health restrictions or negotiation appear, routes to human review.

**Phone Screen Action**

- Header: `Agente Vendas`
- Status chip: `modo automatico`
- Message sequence:
  1. Background process card: `Aula experimental concluida ontem`
  2. Background process card: `Separando contexto da aula e horarios disponiveis`
  3. Agent: "Oi, Julia. Tudo bem? A prof Ana comentou que voce foi super bem na aula de ontem. Como voce se sentiu?"
  4. Interested person: "Gostei bastante. Queria ver se consigo fazer 2x por semana."
  5. Background process card: `Consultando planos 2x por semana`
  6. Background process card: `Cruzando preferencia de horario com vagas fixas`
  7. Agent: "Que bom saber. Para 2x por semana, consigo separar ter/qui as 7h ou seg/qua as 18h30. Algum desses encaixa melhor na sua rotina?"
  8. Interested person: "Segunda e quarta as 18h30."
  9. Agent: "Perfeito. Para deixar sua pre-matricula organizada, me confirma seu nome completo e melhor telefone?"
  10. Interested person: "Julia Martins, esse WhatsApp mesmo."
  11. Background process card: `Criando pre-matricula no sistema`
  12. Background process card: `Vinculando horario seg/qua as 18h30`
  13. Agent: "Pronto, Julia. Deixei sua pre-matricula organizada com esse horario."
  14. Agent: "A Ana, responsavel pelo studio, vai te chamar por aqui para finalizar a matricula e combinar os detalhes finais. Obrigado por vir conhecer a gente."
  15. Responsible notification: "Pre-matricula criada: Julia Martins, interesse em 2x por semana, seg/qua as 18h30. Finalizar matricula."
- System card: `Pre-matricula criada`
- Bottom state: `Responsavel do studio vai finalizar a matricula`

**Automation Steps For Mockup**

1. Trial completion card appears.
2. Agent drafts follow-up.
3. Message sends automatically within configured window.
4. Customer answers.
5. Agent offers two fixed schedules.
6. Customer chooses one.
7. Agent asks for basic pre-enrollment data.
8. Customer sends data.
9. Pre-enrollment card appears.
10. Final handoff message appears.

**Tools Needed Later**

- `crm.get_interested_person`
- `schedule.get_trial_status`
- `plans.list_public_options`
- `whatsapp.send_message`
- `schedule.find_available_slots`
- `schedule.create_tentative_hold`
- `crm.mark_plan_interest`
- `task.create_handoff`

**Terminal States**

- `plan_conversation_started`
- `tentative_slot_created`
- `pending_enrollment_created`
- `human_review_required`
- `no_response_after_followup`

## Flow 4: Financeiro - Renewal Reminder To Payment Link Sent

**Landing job**: Show that monthly fees and renewals are not forgotten until the end of the month.

**Autonomous outcome**: The agent reminds the student, sends the configured payment link/Pix and records the payment status without human participation.

**Trigger**

- Plan expires in 7 days.
- Monthly fee is due tomorrow.
- Monthly fee is overdue within an approved reminder window.

**Customer Action**

1. Student receives a friendly reminder.
2. Student asks for payment link or Pix.
3. Agent sends configured payment instructions.
4. Student confirms payment.
5. Agent confirms the payment, renews the plan and sends final details.

**AI Action**

1. Checks payment status, due date and approved reminder rule.
2. Sends a contextual reminder with no pressure.
3. If configured, sends Pix/link already created by the studio system.
4. Confirms payment status when the student pays.
5. Renews the plan automatically when payment is confirmed.
6. Sends final renewal details and thanks the student.
7. Hands off for discounts, refunds, cancellation, payment dispute or angry tone.

**Phone Screen Action**

- Header: `Agente Financeiro`
- Status chip: `modo automatico`
- Message sequence:
  1. Background process card: `Plano vence em 3 dias`
  2. Background process card: `Conferindo status de pagamento e horario atual`
  3. Agent: "Oi, Ana. Passando para lembrar que seu plano vence nesta sexta. Quer manter os mesmos horarios para o proximo mes?"
  4. Student: "Quero sim. Pode mandar o Pix?"
  5. Background process card: `Buscando Pix/link configurado pelo studio`
  6. Agent: "Claro. Aqui esta o Pix/link do studio para renovar seu plano: [link configurado]."
  7. Student: "Pronto, acabei de pagar."
  8. Background process card: `Confirmando pagamento recebido`
  9. Background process card: `Renovando plano e mantendo horarios atuais`
  10. Agent: "Pagamento confirmado, Ana. Seu plano foi renovado e seus horarios continuam os mesmos para o proximo mes."
  11. Agent: "Obrigado. Qualquer ajuste de horario, pode me chamar por aqui."
  12. Responsible notification: "Plano renovado: Ana. Pagamento confirmado e horarios mantidos para o proximo mes."
- System card: `Plano renovado`
- Payment status pill: `Pagamento confirmado`
- Bottom state: `Renovacao concluida automaticamente`

**Automation Steps For Mockup**

1. Due-date card appears.
2. Agent sends reminder.
3. Student asks for Pix/link.
4. Agent sends configured payment link or Pix instructions.
5. Student confirms payment.
6. Payment is confirmed.
7. Plan is renewed.

**Tools Needed Later**

- `billing.get_student_status`
- `billing.get_payment_link`
- `whatsapp.send_message`
- `billing.mark_conversation_status`
- `task.create_handoff`

**Terminal States**

- `reminder_sent`
- `payment_link_sent`
- `payment_promise_recorded`
- `paid_confirmed`
- `human_review_required`

## Flow 5: Retencao - Inactive Student To Return Class Booked

**Landing job**: Show that the studio notices students drifting away before they cancel.

**Autonomous outcome**: The agent notices inactivity, starts a careful conversation, rebuilds confidence and books a low-friction return class when the student is ready.

**Trigger**

- Student has not attended for an approved number of days.
- Student frequency dropped compared with their usual pattern.
- Student missed multiple classes without rescheduling.

**Customer Action**

1. Student receives a warm check-in.
2. Student answers with hesitation or context.
3. Agent reassures the student without pressure.
4. Agent offers a soft return path.
5. Student asks for an option.
6. Agent offers compatible class options based on their previous pattern.
7. Student chooses one.
8. Agent books the return class and confirms.

**AI Action**

1. Detects inactivity or frequency drop.
2. Checks historical preferred times and teacher/class context.
3. Chooses a warm message template approved by the studio.
4. Starts with a low-pressure check-in, not an immediate scheduling push.
5. If the student shows openness, offers a soft return path.
6. If the student asks for options, finds compatible class times.
7. If student accepts, reserves a compatible class option.
8. If student mentions pain, health, cancellation or personal issue, pauses and routes to human.

**Phone Screen Action**

- Header: `Agente Retencao`
- Status chip: `modo automatico`
- Message sequence:
  1. Background process card: `18 dias sem aula detectados`
  2. Background process card: `Consultando historico: costuma vir ter/qui as 7h`
  3. Agent: "Oi, Marina. Tudo bem? A gente percebeu que voce nao conseguiu vir nas ultimas semanas e quis saber como voce esta."
  4. Student: "Oi. Estou bem, so acabei saindo da rotina."
  5. Agent: "Acontece. Se voce quiser voltar aos poucos, posso procurar um horario mais tranquilo para retomar sem pressa."
  6. Student: "Acho que seria bom. Tem algum horario mais vazio?"
  7. Background process card: `Buscando turma tranquila para retorno`
  8. Background process card: `Priorizando horario parecido com rotina anterior`
  9. Agent: "Tenho quinta as 7h com uma turma menor, ou sexta as 16h. Qual ficaria mais leve para voce?"
  10. Student: "Quinta as 7h."
  11. Background process card: `Reservando aula de retorno e avisando professora`
  12. Agent: "Combinado. Reservei quinta as 7h para voce voltar com calma. A prof Ana vai estar ciente para adaptar a aula se precisar."
  13. Responsible notification: "Aula de retorno marcada: Marina, quinta as 7h. Aluna estava 18 dias sem aula e pediu retomada com calma."
- System card: `18 dias sem aula`
- Mini panel: `Horario comum: ter/qui 7h`
- Bottom state: `Aula de retorno reservada`

**Automation Steps For Mockup**

1. Inactivity card appears.
2. Historic pattern highlights.
3. Agent sends warm check-in.
4. Student replies.
5. Two compatible options appear.
6. Student chooses one.
7. Return class card appears.

**Tools Needed Later**

- `attendance.detect_inactivity`
- `students.get_preferred_times`
- `schedule.find_available_slots`
- `whatsapp.send_message`
- `schedule.create_tentative_hold`
- `attendance.mark_return_plan`
- `task.create_handoff`

**Terminal States**

- `return_slot_created`
- `return_class_booked`
- `student_paused`
- `no_response_after_checkin`
- `human_review_required`

## Landing Implementation Notes

These flows should become the source for:

- WhatsApp conversation mockups in `Quero que meus agentes cuidem de`;
- agent-specific phone screens in `Agentes em acao`;
- animated flow steps inside `Como funciona`;
- SaaS mockup status rows in `Tudo que hoje fica espalhado`;
- future data structures under `data/landing/niches/pilates.ts`.

Recommended visual pattern for each phone flow:

1. A WhatsApp conversation column where messages appear automatically in sequence.
2. A compact system card showing the detected signal or completed action.
3. Background process cards between messages showing what the AI checks or updates silently.
4. Optional choice chips rendered as part of the automatic conversation, not as copiloto controls.
5. A small status/result strip.
6. One visible agent color/persona.
7. No approve/edit/send controls in these phone mockups; those belong only to human-control sections.

Every completed flow should also trigger a responsible-person notification:

- The student/interested-person conversation remains autonomous.
- After something is booked, resolved, renewed or marked, the responsible person receives a short internal WhatsApp-style notification or the SaaS panel shows a notification toast.
- The notification must summarize what happened, who was involved, what changed in the system and whether any human follow-up is needed.
- This notification is informational, not an approval step.

## Not Primary Autonomous WhatsApp Flows

`Gestao` and `Historico/Evolucao` remain important, but they are better shown as SaaS panels or human-assist screens:

- `Gestao`: priority panel, money summary, weekly digest.
- `Historico/Evolucao`: context before class, restrictions, observations and teacher notes.

They can send summaries or reminders later, but they should not be the first 5 WhatsApp-autonomous flows shown on the landing.
