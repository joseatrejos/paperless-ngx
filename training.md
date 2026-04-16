# Paperless-ngx — Training Guide


## Module 1 — What Is This System and Why Use It

- The system is a digital document archive. You upload documents (PDFs, scans, Word files, emails) and it stores them, reads their text, and makes everything searchable.
- Instead of hunting through folders or physical files, you type a word and instantly find every document that contains it.
- Every document can be labeled with tags, a correspondent (who it's from/to), a document type (invoice, contract, etc.), and custom fields.
- The system can learn your labeling habits and start labeling documents automatically.
- Documents never leave your server — everything stays private.

**Key concepts to understand before starting:**
- **Tags** — labels you attach to documents (e.g., "urgent", "taxes-2025", "paid")
- **Correspondent** — the person or company the document is from or addressed to (e.g., "IMSS", "CFE", "John Smith")
- **Document Type** — the category of the document (e.g., Invoice, Contract, Bank Statement)
- **Inbox** — newly uploaded documents that haven't been reviewed yet appear here

---

## Module 2 — Uploading Your First Document

**Goal:** Get a document into the system.

**Option A — Drag and drop from your browser:**
1. Open the app in your browser.
2. Drag any PDF, image, Word, or Excel file directly onto any page.
3. A green progress indicator appears. Wait for it to finish.
4. The document will appear in your document list within a few seconds.

**Option B — Use the upload button:**
1. Click the upload button (top-right area of any page).
2. Select a file from your computer.
3. Wait for processing to complete.


**Option C — Forward emails:**
- If email is configured, forwarding an email with an attachment to the configured address will automatically import the attachment.

**What happens after upload:**
- The system reads (OCR) the document text so you can search by content later.
- It creates a searchable copy.
- It tries to automatically suggest or assign tags, correspondent, and document type based on what it has learned.

---

## Module 3 — Finding Documents

**Goal:** Locate a specific document quickly.

**Search by any word in the document:**
1. Click the search bar at the top.
2. Type any word that appears in the document (e.g., "IMSS", "state of account", "contract renewal").
3. Results update as you type.

**Filter the list to narrow down results:**
- Click **Filters** in the document list.
- Filter by: tag, correspondent, document type, date range, or custom field.
- Combine multiple filters at the same time.

**Use saved views to access frequent searches instantly:**
- A saved view is a pre-configured filter that appears in your sidebar or dashboard.
- Example: a saved view called "Inbox" shows all documents with no tags. Another called "Invoices 2025" shows all invoices from that year.
- To create one: set your filters, then click **Save View**.

**Find documents similar to one you already have:**
- Open a document and scroll to the **Similar Documents** section.
- The system shows other documents with related content.

---

## Module 4 — Organizing a Document (Manually)

**Goal:** Add labels to a document so it's easy to find later.

1. Click on any document to open it.
2. On the right panel you will see fields: **Title**, **Correspondent**, **Document Type**, **Date**, **Tags**, and any custom fields.
3. Edit each field:
   - **Title** — Give it a clear name (e.g., "CFE Invoice March 2025")
   - **Correspondent** — Who sent or received this? (e.g., "CFE")
   - **Document Type** — What kind of document is it? (e.g., "Invoice")
   - **Date** — The date on the document, not the upload date
   - **Tags** — Add any relevant labels (e.g., "electricity", "paid", "2025")
4. Changes are saved automatically.

**Tips:**
- Use consistent names for correspondents — "CFE" and "C.F.E." will create two different correspondents.
- Tags can be nested: "expenses > utilities > electricity" for better organization.
- The system will start learning your labeling patterns and suggest them automatically over time.

---

## Module 5 — Creating Tags, Correspondents, and Document Types

**Goal:** Set up the labels your organization will use consistently.

**Creating a Tag:**
1. Go to **Tags**.
2. Click **Add Tag**.
3. Give it a name and optionally a color.
4. You can nest it under a parent tag (e.g., parent: "Expenses", child: "Utilities").

**Creating a Correspondent:**
1. Go to **Manage → Correspondents**.
2. Click **Add Correspondent**.
3. Enter the name exactly as you want it to appear on documents.
4. Optionally add matching rules so documents from this sender are auto-assigned.

**Creating a Document Type:**
1. Go to **Manage → Document Types**.
2. Click **Add Document Type**.
3. Enter the name (e.g., "Invoice", "Contract", "Pay Stub").
4. Optionally add matching rules.

**Adding a matching rule (automatic assignment):**
- When creating or editing a tag/correspondent/type, look for the **Matching** section.
- Set the **Algorithm** (e.g., "Any word") and the **Pattern** (words to look for in the document text).
- Example: Correspondent "CFE" with pattern "Comisión Federal de Electricidad" — every document containing that phrase will be auto-assigned to CFE.

---

## Module 6 — Setting Up Automatic Organization with Workflows

**Goal:** Make the system automatically tag, label, and organize documents when they arrive, so you don't have to do it manually.

**What is a Workflow?**
A workflow is a rule: "When X happens, do Y." For example: "When a document arrives that contains the word 'nómina', add the tag 'Payroll' and set the document type to 'Pay Stub'."

**Creating a basic auto-labeling workflow:**
1. Go to **Manage → Workflows**.
2. Click **Add Workflow**.
3. Give it a descriptive name (e.g., "Auto-tag payroll documents").
4. Set the **Trigger**:
   - Choose **Document Added** (fires when a new document is fully processed).
   - Under **Filter**, set conditions — for example: **Content contains** → type "nómina".
5. Set the **Action**:
   - Choose **Assignment**.
   - Fill in what to assign: tags, correspondent, document type, storage path, or title.
6. Save the workflow.

**Common workflow recipes:**

| You want to… | Trigger | Filter | Action |
|---|---|---|---|
| Auto-tag electricity bills | Document Added | Content contains "CFE" or "Comisión Federal" | Add tag "Utilities", set correspondent "CFE", set type "Invoice" |
| Auto-tag payroll documents | Document Added | Content contains "nómina" or "IMSS" | Add tag "Payroll", set type "Pay Stub" |
| Auto-tag contracts | Document Added | Content contains "contrato" | Add tag "Contracts", set type "Contract" |
| Notify by email when a document arrives | Document Added | Any filter | Action: Email — send to your address |
| Move old documents to trash automatically | Scheduled | Documents older than X with a specific tag | Action: Move to Trash |

**Tips:**
- Workflows are processed in order. Lower order number = higher priority.
- You can have multiple actions in one workflow.
- Test with a few documents before enabling on all documents.

---

## Module 7 — Working with Multiple Documents at Once

**Goal:** Apply changes to many documents in one go.

1. In the document list, check the box next to each document you want to select (or use **Select All**).
2. A bulk action toolbar appears at the top.
3. Choose what to do:
   - **Assign tags / correspondent / document type** — applies to all selected documents
   - **Download** — downloads all selected as a ZIP file
   - **Delete** — moves all selected to trash
   - **Merge** — combines selected documents into a single new document
   - **Send to Documenso** — sends all selected for digital signing

---

## Module 8 — Sharing a Document

**Goal:** Give someone else access to a document.

**Share a public link (no login required):**
1. Open the document.
2. Click the **Share** button.
3. Click **Create Share Link**.
4. Set an optional expiration date.
5. Copy the link and send it to whoever needs it.

**Share with another user of the system:**
1. Open the document.
2. Go to the **Permissions** tab.
3. Add the user or group and choose whether they can view or also edit.

**Email a document directly:**
1. Open the document.
2. Click the **Send** button → **Email**.
3. Enter the recipient's address, subject, and message.
4. The document will be attached and sent.

---

## Module 9 — Sending a Document for Digital Signing (Documenso)

**Goal:** Send a document to Documenso so it can be signed digitally.

**Before you start:** Documenso must be configured by your administrator (URL and token set in configuration, and the Team Slug set in the app settings page). If it's not configured, you'll see an error message with a link to the configuration page.

**From a single document:**
1. Open the document.
2. Click the **Send** button → **Sign with Documenso**.
3. You will be redirected to the Documenso interface to set up signature fields and send to signers.

**From multiple documents at once:**
1. Select multiple documents using the checkboxes in the document list.
2. In the bulk toolbar, click **Send to Documenso**.

---

## Module 10 — Setting Up Email Import (IMAP)

**Goal:** Have the system automatically import documents from a dedicated email inbox.

1. Go to **Settings → Mail Accounts**.
2. To connect via **standard IMAP**: Click **Add Mail Account** and enter your IMAP server details, then save and verify the connection.
3. To connect via **Gmail or Outlook OAuth** (if configured by your administrator): Click the **Connect Gmail Account** or **Connect Outlook Account** button directly on the Mail Settings page. This will redirect you to Google or Microsoft to authorize access — no IMAP credentials needed.

   > **Note:** The OAuth buttons only appear if your administrator has set up the OAuth app credentials in the server configuration. If you don't see them, use the standard IMAP option instead.
4. Go to **Settings → Mail Rules**.
5. Click **Add Mail Rule**.
6. Configure:
   - **Account** — the account you just added
   - **Folder** — which IMAP folder to watch (e.g., "Inbox" or "Paperless")
   - **Filter** — optionally filter by subject, sender, or body text
   - **Action** — what to consume: attachment only, or the full email as a PDF
   - **Post-consume** — what to do with the email after: mark as read, delete, move to folder
7. Save. The system checks for new emails automatically every 10 minutes.

**Practical tip:** Create a dedicated email address (e.g., `documents@yourcompany.com`) and forward invoices, receipts, and contracts there. Set a rule that watches that folder. Every forwarded email gets automatically imported.

---

## Module 11 — Using the Dashboard

**Goal:** Set up a personalized home screen with quick access to what matters most.

- The dashboard shows **Saved Views** as widgets — each widget is a filtered document list.
- Example widgets: "Inbox" (unreviewed documents), "Invoices this month", "Contracts expiring soon".

**Adding a widget to the dashboard:**
1. Go to **Manage → Saved Views**.
2. Create or edit a saved view.
3. Enable the **Show on Dashboard** toggle.
4. Go back to the dashboard — the widget appears.

**Rearranging the dashboard:**
- Drag and drop widgets to change their order.

---

## Module 12 — Reviewing and Clearing the Inbox

**Goal:** Process newly arrived documents and make sure they are properly labeled.

The "Inbox" is a saved view that shows all documents that don't have any tags yet (or have an "inbox" tag, depending on setup).

**Daily workflow:**
1. Open the **Inbox** view from the sidebar or dashboard.
2. Click each document.
3. Review the auto-suggested metadata (shown in the right panel with a suggestion indicator).
4. Accept or correct: title, correspondent, document type, date, tags.
5. Once labeled, the document automatically disappears from the inbox.

**If you see suggestions from the AI/classifier:**
- A small icon appears next to fields that have suggestions.
- Click to accept the suggestion or type a different value.

---

## Module 13 — Managing Users and Access

**Goal:** Control who can see and edit which documents.

**Adding a new user:**
1. Go to **Settings → Users & Groups**.
2. Click **Add User**.
3. Set their username, email, and password.
4. Assign them to a group if you use groups for role-based access.

**Creating a group:**
1. Go to **Settings → Users & Groups → Groups**.
2. Create a group (e.g., "Accounting", "HR").
3. Assign permissions: which types of objects they can create, view, edit, or delete.

**Making a document private or shared:**
- By default, new documents are visible only to the person who uploaded them (or based on your default permissions setting).
- To share a document with a team, open it → **Permissions tab** → add the group with View or Edit access.

**Setting default permissions for everything you upload:**
1. Go to your **User Profile** (click your avatar, top right).
2. Under **Default Permissions**, set which users/groups automatically get access to documents you create.

---

## Module 14 — Trash and Recovery

**Goal:** Safely delete documents and recover them if needed.

**Deleting a document:**
- Open the document → click the **Delete** button.
- The document moves to the **Trash** — it is NOT permanently deleted yet.

**Recovering a deleted document:**
1. Go to **Trash** in the left sidebar.
2. Find the document and click **Restore**.

**Permanently deleting:**
- In Trash, click **Delete Permanently** on a document, or click **Empty Trash** to permanently delete everything in trash.
- After permanent deletion, the document cannot be recovered.

---

## Module 15 — Searching Like a Pro

**Goal:** Find exactly what you need using advanced search techniques.

| What you want | How to do it |
|---|---|
| Documents containing a specific phrase | Type the exact phrase in the search bar |
| Documents from a specific person | Filter by **Correspondent** |
| All invoices from last year | Filter by **Document Type = Invoice** + **Date range = 2024** |
| Documents with a specific custom field value | Use the **Filter** panel → **Custom Fields** |
| Documents similar to one you're viewing | Open the document → scroll to **Similar Documents** |
| Documents you haven't reviewed yet | Open the **Inbox** saved view |

**Tips:**
- The search reads the full text of each document, including handwritten text that was scanned.
- You can combine search text with filters for precise results.
- Save any combination of filters as a Saved View for one-click access later.

---

## Module 16 — Custom Fields

**Goal:** Add your own data fields to documents beyond the default ones.

Custom fields let you store information specific to your organization. Examples:
- **Invoice Number** (text)
- **Amount Paid** (monetary)
- **Contract Expiry Date** (date)
- **Signed?** (checkbox/boolean)
- **Related Contract** (link to another document)

**Creating a custom field:**
1. Go to **Manage → Custom Fields**.
2. Click **Add Custom Field**.
3. Name it and choose its type (text, number, date, checkbox, dropdown, document link, etc.).

**Using a custom field:**
- Open any document.
- In the right panel, click **Add Field** and choose your custom field.
- Enter the value.

**Filtering by custom field:**
- In the document list, open **Filters → Custom Fields** and search by field value.

---

## Module 17 — Frequently Asked Questions

**Q: I uploaded a document but the text is wrong or missing — why?**
The document may be a scanned image without embedded text. The system tries to OCR it automatically. If the scan quality is poor (blurry, dark, skewed), text extraction may be incomplete. Try re-scanning at a higher resolution (300 DPI or more).

**Q: The automatic tags/correspondent are wrong — how do I fix it?**
Manually correct the values in the document. The system learns from your corrections over time. The more consistently you label documents, the better the automatic suggestions become.

**Q: I deleted a document by accident — can I get it back?**
Yes. Go to **Trash** in the sidebar and click **Restore**. Documents stay in trash until you permanently delete them or the automatic purge runs.

**Q: Can two people use the system at the same time?**
Yes. Multiple users can be logged in and working simultaneously.

**Q: Can I see who made changes to a document?**
Yes, if your administrator has enabled the audit log. Open the document and look for the **Audit Trail** tab.

**Q: How do I change my password?**
Click your avatar (top right) → **Profile** → **Change Password**.

**Q: How do I enable two-factor authentication (2FA)?**
Click your avatar → **Profile** → scroll to the **Two-Factor Authentication** section → follow the QR code setup steps.

**Q: Can I access the system from my phone?**
Yes. The system works in any modern mobile browser. There is no dedicated mobile app, but the web interface adapts to smaller screens.
