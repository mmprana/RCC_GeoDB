# Uploading the RCC GeoDB Package to GitHub

The repository is:

```text
https://github.com/mprgesru/RCC_GeoDB
```

The simplest method is the GitHub website. Use GitHub Desktop if you will keep updating the repository.

---

## Option A — Upload through the GitHub website

### 1. Prepare the files

Download and unzip:

```text
RCC_GeoDB_Upload.zip
```

You should see:

```text
README.md
rcc_schema.py
create_rcc_gdb.py
validate_schema.py
export_data_dictionary.py
RCC_Data_Dictionary.csv
RCC_Domains.csv
RCC_Layer_Summary.csv
RCC_Relationships.csv
article/
```

### 2. Open the repository

Go to:

```text
https://github.com/mprgesru/RCC_GeoDB
```

Sign in as the account that owns the repository.

### 3. Start the upload

Click:

```text
Add file → Upload files
```

### 4. Drag the files

Drag the **contents** of the unzipped folder into the upload area.

Do not drag the outer folder if it creates an unnecessary nested folder. You want `README.md` at the repository root and `article/` as a folder.

### 5. Commit

Use a message such as:

```text
Add RCC GeoDB and article package
```

Click:

```text
Commit changes
```

### 6. Verify

Check that these exist in the repository:

- `README.md`
- `rcc_schema.py`
- `create_rcc_gdb.py`
- `article/MANUSCRIPT_DRAFT.md`
- `article/interviews/INTERVIEW_GUIDE.md`

If GitHub says there are too many files, upload in three batches:

1. Root scripts and CSV files.
2. `article/` top-level files.
3. `article/interviews/` files.

GitHub’s browser uploader generally accepts up to 100 files per upload.

---

## Option B — GitHub Desktop

### 1. Install GitHub Desktop

Download from:

```text
https://desktop.github.com/
```

### 2. Sign in

Sign in with the GitHub account that owns `mprgesru/RCC_GeoDB`.

### 3. Clone the repository

```text
File → Clone repository → URL
```

Enter:

```text
https://github.com/mprgesru/RCC_GeoDB.git
```

Choose a local folder.

### 4. Copy the files

Copy the contents of the unzipped package into the cloned repository folder.

### 5. Commit

GitHub Desktop will show the new files.

Enter a summary:

```text
Add RCC GeoDB and article package
```

Click:

```text
Commit to main
```

### 6. Push

Click:

```text
Push origin
```

If push fails, check that you are signed in as the repository owner and that the repository is not archived.

---

## Option C — Command line with a personal access token

Use this only if you are comfortable with Git.

### 1. Create a fine-grained token

GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token.

Repository access:

```text
Only select repositories → mprgesru/RCC_GeoDB
```

Permissions:

```text
Contents: Read and write
Metadata: Read-only
```

Generate and copy the token.

### 2. Push

```bash
cd /path/to/RCC_GeoDB_repo
git remote set-url origin https://github.com/mprgesru/RCC_GeoDB.git
git push -u origin main
```

When prompted:

```text
Username: mprgesru
Password: paste the token
```

Do not use your GitHub account password.

### 3. If you still get 403

Check:

- Are you signed in as the repository owner?
- Does the token have **Contents: Read and write**?
- Is the repository owned by a different account or organisation?
- Is the repository archived?
- Is branch protection blocking the push?
- If the repository is in an organisation, has SSO been authorised for the token?

---

## Why the earlier push failed

The error was:

```text
Permission to mprgesru/RCC_GeoDB.git denied to mprgesru.
HTTP 403
```

This means the authenticated credential did not have write access to the repository. The files and commits are fine. The problem is account permission or token scope, not the code.

---

## Recommended choice

Use **Option A** for the first upload. It is the fastest and avoids Git authentication.

Use **Option B** afterwards if you want to keep updating the repository from your computer.
