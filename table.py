def generate_latex_table_from_file(file_path):
    try:
        # Read data from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Start building the LaTeX table
        latex_table = [
        "\\begin{longtable}{|c|c|c|c|c|c|c|c|}",
        "\\hline",
        "\\textbf{Instância} & \\textbf{Algoritmo}  & \\textbf{Limiar} & \\textbf{Resultado} & \\textbf{Qualidade} & \\textbf{Tempo(s)} & \\textbf{Bytes} \\\\",
        "\\hline",
        "\\endfirsthead",  # Add header on subsequent pages
        "\\multicolumn{8}{c}%",
        "{{\\tablename\\ \\thetable{} -- Continuação}} \\\\",
        "\\hline",
        "\\textbf{Instância} & \\textbf{Algoritmo} & \\textbf{Limiar} & \\textbf{Resultado} & \\textbf{Qualidade} & \\textbf{Tempo(s)} & \\textbf{Bytes} \\\\",
        "\\hline",
        "\\endhead",  # Header for subsequent pages
        "\\hline",
        "\\endfoot",
        "\\hline"
        ]

        # Process each line of the file and add to the table
        for line in lines[1:]:  # Skip the header line
            # Remove extra spaces and newlines
            data = line.strip().split(',')
            # Check if the line has the correct number of columns
            if len(data) == 8:

                #remove coluna Nós

                data.pop(2)

                # Round the quality to two decimal places
                # Replace '%' with 'x'
                data[5] =  f"{float(data[5]):.2f}"
                # Replace 'Twice Around the Tree' with 'TATT'
                data[1] = 'TATT' if data[1] == 'Twice Around the Tree' else data[1]
                # Replace 'Christofides' with 'CRIS'
                data[1] = 'CHRI' if data[1] == 'Christofides' else data[1]
                #truncate the resuly to two decimal places
                data[3] = f"{float(data[3]):.2f}"
                #truncate the quality to two decimal places
                data[4] = f"{float(data[4]):.2f}"
                # Truncate the execution time to two decimal places
               
                # Add the formatted line to the table
                latex_table.append(" & ".join(data) + " \\\\")
            else:
                print(f"Invalid or insufficient data in line: {line}")

        # Finish the table
        latex_table.extend([
            "\\hline",
            "\\caption{Comparison of Algorithms TATT and CRIS}",
            "\\label{tab:algorithms_comparison}",
            "\\end{longtable}"
        ])

        return "\n".join(latex_table)

    except FileNotFoundError:
        return "File not found."

# Caminho do arquivo de dados
file_path = "results.csv"  # Substitua pelo caminho correto do seu arquivo CSV

# Gerar a tabela em LaTeX
latex_table_content = generate_latex_table_from_file(file_path)
print(latex_table_content)