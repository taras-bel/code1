# Supabase: Полная настройка для NoaMetrics

## 1. Создание проекта
- Зарегистрируйтесь на https://supabase.com/
- Создайте новый проект (укажите название, регион, пароль для базы).

## 2. Таблицы (SQL)
Перейдите в Supabase → SQL Editor → New Query и выполните по очереди:

### Таблица profiles
```sql
create table profiles (
  id uuid primary key,
  email text unique not null,
  full_name text not null,
  phone text
);
```

### Таблица rate_limits
```sql
create table rate_limits (
  user_id uuid primary key references profiles(id),
  analysis_count int default 0,
  last_analysis timestamptz,
  week_start timestamptz,
  max_weekly_analyses int default 3
);
```

### Таблица analyses
```sql
create table analyses (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id),
  job_description text,
  status text default 'pending',
  results jsonb,
  created_at timestamptz default now()
);
```

### Таблица uploaded_files
```sql
create table uploaded_files (
  id uuid primary key default gen_random_uuid(),
  filename text not null,
  file_path text not null,
  file_type text,
  file_size int,
  created_at timestamptz default now(),
  user_id uuid references profiles(id),
  analysis_id uuid references analyses(id)
);
```

## 3. Storage Bucket
- Перейдите в Storage → Create bucket
- Название: `cv-uploads`
- Public: **Да** (или настройте RLS для приватности)

## 4. Row Level Security (RLS)
Включите RLS для всех таблиц и добавьте политики:

### Пример для uploaded_files
```sql
alter table uploaded_files enable row level security;
create policy "Users can view their files" on uploaded_files
  for select using (auth.uid() = user_id);
create policy "Users can insert their files" on uploaded_files
  for insert with check (auth.uid() = user_id);
create policy "Users can delete their files" on uploaded_files
  for delete using (auth.uid() = user_id);
```

Аналогично для других таблиц (profiles, analyses, rate_limits) — разрешить доступ только владельцу.

## 5. Auth
- Включите Email Auth (или Google Auth, если нужно).
- Получите Service Role Key и URL проекта для backend.

## 6. Переменные окружения для backend
```
SUPABASE_URL=... (ваш url)
SUPABASE_SERVICE_ROLE_KEY=... (ваш service role key)
```

---

**Теперь Supabase полностью готов для работы с этим проектом!** 