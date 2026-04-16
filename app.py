import pikepdf
from flask import Flask, request, send_file
import io

app = Flask(__name__)

@app.route('/decrypt', methods=['POST'])
def decrypt_pdf():
    # 確認是否有收到檔案與密碼
    if 'file' not in request.files or 'password' not in request.form:
        return "缺少檔案或密碼", 400
        
    password = request.form.get('password')
    file = request.files['file']

    try:
        # 使用 pikepdf 打開加密的 PDF
        pdf = pikepdf.open(file, password=password)
        
        # 將解密後的 PDF 存入記憶體緩衝區 (不落地存檔，確保安全)
        out_pdf = io.BytesIO()
        pdf.save(out_pdf)
        out_pdf.seek(0)
        
        # 回傳解密後的 PDF 檔案
        return send_file(out_pdf, mimetype='application/pdf', download_name='decrypted.pdf')
    except pikepdf.PasswordError:
        return "密碼錯誤", 401
    except Exception as e:
        return str(e), 500

# 提供一個簡單的根目錄檢查伺服器是否存活
@app.route('/', methods=['GET'])
def health_check():
    return "解密伺服器運作中！", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)