﻿using Microsoft.EntityFrameworkCore;
using STRATFY.Helpers;
using STRATFY.Interfaces.IRepositories;
using STRATFY.Models;

namespace STRATFY.Repositories
{
    public class RepositoryBase<T> : IRepositoryBase<T>, IDisposable where T : class
    {
        
        public AppDbContext contexto;
        public bool saveChanges = true;
        DbSet<T> _dbSet;

        public RepositoryBase(AppDbContext context, bool pSaveChanges = true)
        {
            contexto = context;
            saveChanges = pSaveChanges;
            
        }
        public async Task<List<T>> SelecionarTodosAsync()
        {
            return await contexto.Set<T>().ToListAsync();
        }

        public async Task<T> SelecionarChaveAsync(params object[] variavel)
        {
            return await contexto.Set<T>().FindAsync(variavel);
        }

        public async Task<T> IncluirAsync(T entity)
        {
            await contexto.Set<T>().AddAsync(entity);
            if (saveChanges)
            {
                await contexto.SaveChangesAsync();
            }
            return entity;
        }

        public async Task<T> AlterarAsync(T entity)
        {
            contexto.Entry<T>(entity).State = EntityState.Modified;
            if (saveChanges)
            {
                await contexto.SaveChangesAsync();
            }
            return entity;
        }

        public async Task ExcluirAsync(T entity)
        {
            contexto.Entry<T>(entity).State = EntityState.Deleted;
            if (saveChanges)
            {
               await contexto.SaveChangesAsync();
            };
        }

        public List<T> SelecionarTodos()
        {
            return contexto.Set<T>().ToList();
        }

        public T SelecionarChave(params object[] variavel)
        {
            return contexto.Set<T>().Find(variavel);
        }

        public T Incluir(T entity)
        {
            contexto.Set<T>().Add(entity);
            if (saveChanges)
            {
                contexto.SaveChanges();
            }
            return entity;
        }

        public T Alterar(T entity)
        {
            contexto.Entry<T>(entity).State = EntityState.Modified;
            if (saveChanges)
            {
                contexto.SaveChanges();
            }
            return entity;
        }

        public void Excluir(T entity)
        {
            contexto.Entry<T>(entity).State = EntityState.Deleted;
            if (saveChanges)
            {
                contexto.SaveChanges();
            }
        }

        public void Dispose()
        {
            contexto.Dispose();
        }

        public void Salvar()
        {
            contexto.SaveChanges();
        }
    }
}














