# Four worked examples

These inputs and outputs are illustrative, not measured host benchmarks. The useful result can be shorter or longer depending on your material. Replace the example with your own information and remove secrets before sharing it.

Examples use Codex's `$skill-name`. In Claude, select `/practical-work-kit:skill-name` and paste the same material. For example, replace `$check-my-work` with `/practical-work-kit:check-my-work`. Installation and the four command names are in [the README](../README.md).

## 1. Check a budget

**Request**

```text
Use $check-my-work to check this event budget. Tell me whether it is ready to use.
Venue: 3,000. Materials: 2,000. Listed total: 6,000.
I have not provided receipts or confirmed tax.
```

**Useful answer**

> Correct the total: 3,000 + 2,000 = 5,000. The listed total is 1,000 too high. This check covers the listed arithmetic; receipts and tax remain unverified. Fix the total, then confirm whether tax is included.

The check should identify the actual arithmetic error and say what remains unknown. It should not invent extra fees or demand an unrelated checklist.

## 2. Challenge a plan

**Request**

```text
Use $challenge-my-plan to challenge this plan.
I want to build a complete time-management app in four weeks, but I have not spoken to any users.
The goal is to find out whether freelancers would use it. I have six hours a week.
```

**Useful answer**

> Start smaller. The key assumption is that freelancers need your proposed scheduling approach. Four weeks gives you only 24 hours, and building the complete app would postpone testing that assumption. Make an interactive scheduling mockup and ask a few target users to try it with their own tasks. If they do not want to use it again, revise the problem and workflow before building more.

The user can propose or change the test. A synthetic critique is not evidence of demand and is not an independent reviewer unless a separate reviewer actually participates.

## 3. Shape an idea

**Request**

```text
Use $shape-my-idea to give me three titles for a five-minute video.
Topic: organizing a small work desk. Audience: people new to working from home.
Keep the tone friendly and the idea easy to film this weekend.
```

**Useful answer**

> 1. A Clearer Desk in Five Minutes
> 2. Small Desk, Easier Work: Start with These Three Changes
> 3. A Better Workday Starts with Your Desk

Three titles are the requested deliverable. The skill should not automatically create a funnel, publish the video, buy ads, or claim guaranteed views.

## 4. Carry context

**Request**

```text
Use $carry-my-context to help me move to a new conversation.
Decided: the event will be on Saturday morning; the budget total is corrected to 5,000.
Completed: invitation draft. Exact draft: "Join us on Saturday morning to organize our work desks!"
Still unconfirmed: venue address and whether tax is included.
Next: confirm the address, then finish the invitation. Sending it has not been authorized.
```

**Useful answer**

> Goal: finish the invitation for the Saturday morning event. The timing is decided and the listed budget total is 5,000.
>
> Keep the exact draft: "Join us on Saturday morning to organize our work desks!" The venue address and tax are still unconfirmed.
>
> Next: confirm the address, then finish the invitation. It has not been sent, and sending it has not been authorized. Bring the original attachments into the next conversation if they need checking.

The note preserves the actual draft and authorization boundary. It does not convert an old note into permission for external actions or claim files were transferred.
