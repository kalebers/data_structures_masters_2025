import statistics

# Imprime, em formato de tabelas, os dados coletados
def generate_html(results_per_size, type): 
    
    # Início do HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Resultados dos Algoritmos de {type}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h2 {{ margin-top: 40px; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 40px; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .highlight {{ background-color: #d4edda; font-weight: bold; }}  /* para destacar os valores mais eficientes */
        </style>
    </head>
    <body>
        <h1>Resultados de Desempenho dos Algoritmos de {type}</h1>
    """
    
    # Para cada tamanho de array, imprime uma tabela com os tempos e memórias utilizados por algoritmo
    for size, metrics in results_per_size.items():
        algorithms = metrics["time"].keys()
        avg_times = {}
        avg_mems = {}
        
        # Primeiro, calcular tempos e memórias para comparação
        for algorithm in algorithms:
            if len(metrics["time"][algorithm]) > 1:
                avg_times[algorithm] = statistics.mean(metrics["time"][algorithm])  
            if len(metrics["used_memory"][algorithm]) > 1:
                avg_mems[algorithm] = statistics.mean(metrics["used_memory"][algorithm]) 
        
        # Encontrar os mais rápidos, para poder deixar de outra cor
        min_time = min(avg_times.values())
        min_mem = min(avg_mems.values())
    
        html += f"<h2>Tamanho do array: {size}</h2>\n"
        html += """
        <table>
            <tr>
                <th>Algoritmo</th>
                <th>Tempo Médio (s)</th>
                <th>Desvio Tempo (s)</th>
                <th>Memória Média (KB)</th>
                <th>Desvio Memória (KB)</th>
                <th>Rodadas</th>
            </tr>
        """
        
        for algorithm in algorithms:
            times_list = metrics["time"][algorithm]
            mems_list = metrics["used_memory"][algorithm]
            
            # std é o desvio padrão
            avg_time = f"{statistics.mean(times_list):.6f}" if len(times_list) > 1 else '-'
            std_time = f"{statistics.stdev(times_list):.6f}" if len(times_list) > 1 else '-'
            avg_mem = f"{statistics.mean(mems_list):.2f}" if len(mems_list) > 1 else '-'
            std_mem = f"{statistics.stdev(mems_list):.2f}" if len(mems_list) > 1 else '-'
    
            # Adiciona classe .highlight se for o menor
            time_class = "highlight" if avg_time == f"{min_time:.6f}" else ""
            mem_class = "highlight" if avg_mem == f"{min_mem:.2f}" else ""
    
            html += f"""
            <tr>
                <td>{algorithm}</td>
                <td class="{time_class}">{avg_time}</td>
                <td>{std_time}</td>
                <td class="{mem_class}">{avg_mem}</td>
                <td>{std_mem}</td>
                <td>{len(times_list)}</td>
            </tr>
            """
    
        html += "</table>\n"
    
    # Fim do HTML
    html += """
    </body>
    </html>
    """
    
    return html
