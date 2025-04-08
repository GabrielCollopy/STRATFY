﻿using Microsoft.EntityFrameworkCore.Metadata.Internal;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace STRATFY.Models;

public partial class Movimentacao
{
    public int Id { get; set; }

    [Required]
    [ForeignKey("Extrato")]
    public int? ExtratoId { get; set; }
    public virtual Extrato Extrato { get; set; } = null!;

    [Required]
    [ForeignKey("Categoria")]
    public int? CategoriaId { get; set; }
    public virtual Categoria Categoria { get; set; } = null!;

    public string? Descricao { get; set; }

    public string Tipo { get; set; } = null!;

    public decimal Valor { get; set; }

    public DateOnly DataMovimentacao { get; set; }


}
