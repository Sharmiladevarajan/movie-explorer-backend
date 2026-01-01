# Database Migration Instructions

## Language Column Migration

### Apply Migration
Run this command to add the language column to your database:

```powershell
psql -U postgres -d moviedb -f add_language_column.sql
```

### What This Does
1. Adds a `language` column to the `movies` table
2. Sets default value to 'English' for all existing movies
3. Creates an index for better query performance on language
4. Allows VARCHAR(50) for language names

### Verify Migration
Check if the migration was successful:

```sql
psql -U postgres -d moviedb -c "\d movies"
```

You should see the `language` column in the table structure.

### Rollback (if needed)
If you need to remove the language column:

```sql
psql -U postgres -d moviedb -c "ALTER TABLE movies DROP COLUMN language;"
psql -U postgres -d moviedb -c "DROP INDEX IF EXISTS idx_movies_language;"
```

## After Migration

### Test the Feature
1. Start the backend: `uvicorn app.main:app --reload`
2. Start the frontend: `npm run dev`
3. Create or edit a movie
4. Select a language from the dropdown
5. Save and verify the language appears

### Existing Data
All existing movies will have language set to 'English' by default. You can edit them to set the correct language.

## Demo Data (Optional)

If you want to add sample data with various languages:

```sql
psql -U postgres -d moviedb -f demo_data.sql
```

This will add 15+ movies with different languages and full cast information.

## Troubleshooting

### Error: column "language" already exists
**Solution**: The migration was already applied. No action needed.

### Error: relation "movies" does not exist
**Solution**: Run the schema.sql first to create tables:
```powershell
psql -U postgres -d moviedb -f schema.sql
```

### Error: permission denied
**Solution**: Make sure you're logged in as postgres user or have sufficient permissions.

### Backend Returns 500 Error
**Cause**: Language column doesn't exist yet
**Solution**: Apply the migration and restart the backend

## Best Practices

1. **Backup First**: Always backup your database before migrations
   ```powershell
   pg_dump -U postgres moviedb > backup_before_language.sql
   ```

2. **Test in Development**: Test migrations in a dev environment first

3. **Version Control**: Keep migration files in git

4. **Documentation**: Update README with new features

## Migration Checklist

- [ ] Backup database
- [ ] Review migration SQL
- [ ] Apply migration
- [ ] Verify column exists
- [ ] Restart backend
- [ ] Test in frontend
- [ ] Update documentation
- [ ] Deploy to production (if applicable)

## Next Steps

After applying the migration:
1. Update your README to mention language support
2. Test the cast editing feature
3. Add some movies with different languages
4. Share with users!
