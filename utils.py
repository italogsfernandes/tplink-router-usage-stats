def write_output_to_file(stats, created_date, output_file, output_file_completo):
    with open(output_file, "a+") as file:
        file.write("#"*80 + "\n")
        for stat in stats:
            print(f'{created_date.strftime("%D %T")} | {stat}')
            file.write(f'{created_date.strftime("%D %T")} | {stat}\n')
    
    with open(output_file_completo, "a+") as file:
        for stat in stats:
            file.write(f'{created_date.strftime("%D")}\t')
            file.write(f'{created_date.strftime("%T")}\t')
            file.write(f'{stat.ip}\t')
            file.write(f'{stat.mac}\t')
            file.write(f'{stat.total_byte}\t')
            file.write(f'{stat.apelido}\t')
            file.write(f'{stat.total_best_unit}\t')
            file.write(f'{stat.total_preco:.2f}\t')
            file.write('\n')

